import json

import openai
import requests
import stripe
import tiktoken
from django.http import HttpResponse
from django.views import View

from telegram.utils import create_checkout_session
from telegram.config import *
from telegram.models import TelegramAvatar, TelegramMembership, TelegramUser

stripe.api_key = stripe_secret_key

# Set your OpenAI API key
openai.api_key = openai_api_key


def num_tokens_from_messages(messages):
    # model to encoding mapping https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == 'name':  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        req_body = json.loads(request.body)
       
        # Handle callback
        if "callback_query" in req_body:
            TelegramWebhookView.handle_callbacks(request)
        # Handle Messages and Commands
        elif "message" in req_body:
            TelegramWebhookView.handle_messages_commands(request)

        return HttpResponse('OK')

    @staticmethod
    def handle_callbacks(request):
        req_body = json.loads(request.body)
        bot_id = int(request.GET.get('botid'))
        print(req_body)

        try:
            price_id = req_body['callback_query']["data"]
            chat_id = req_body['callback_query']['message']['chat']['id']

            # Make sure the telegram bot ID is valid
            telegram_avatar = TelegramAvatar.objects.filter(telegram_bot_id=bot_id).first()
            if telegram_avatar is None:
                return

            # Create a checkout session for the product
            checkout_url = create_checkout_session(price_id=price_id, chat_id=chat_id, bot_id=bot_id)
            if checkout_url:
                TelegramWebhookView.send_message(telegram_avatar.telegram_token, chat_id,
                                                 payment_message.format(checkout_url))
            return

        except Exception as e:
            print("Exceptions is" + e)
            return

    @staticmethod
    def handle_messages_commands(request):
        bot_id = int(request.GET.get('botid'))
        req_body = json.loads(request.body)
        print(req_body)
        text = None

        try:
            chat_id = req_body['message']['chat']['id']
            if "text" in req_body['message']:
                text = req_body['message']['text']
            telegram_user_id = req_body['message']['from']['id']
            first_name = req_body['message']['from']['first_name']
            last_name = req_body['message']['from']['last_name']
            name = first_name + ' ' + last_name
        except Exception as e:
            return

        # Make sure the telegram bot ID is valid
        telegram_avatar = TelegramAvatar.objects.filter(telegram_bot_id=bot_id).first()
        if telegram_avatar is None:
            return

        # Show a loader message            
        TelegramWebhookView.send_chat_action(telegram_avatar.telegram_token, chat_id, 'typing')

        # Get or create a TelegramUser
        telegram_user, created = TelegramUser.objects.get_or_create(telegram_user_id=telegram_user_id,
                                                                    defaults={'name': name})

        # Get or create a TelegramMembership
        telegram_membership, created = TelegramMembership.objects.get_or_create(
            telegram_user=telegram_user, telegram_avatar=telegram_avatar,
            defaults={'credits_available': telegram_avatar.free_credits})

        chat_response = None

        if created:
            chat_response = telegram_avatar.welcome_message
        # handle Telegram commands if any in the message
        elif text == '/help':
            chat_response = help_message
        elif text == '/restart':
            telegram_membership.conv_history = []
            telegram_membership.save()
            chat_response = restart_message
        elif text == '/balance':
            chat_response = balance_message.format(telegram_membership.credits_available)
        elif text == '/threestory':
            telegram_membership.stories_per_day = 3
            chat_response = story_freq_message.format(telegram_membership.stories_per_day)
            telegram_membership.save()
        elif text == '/twostory':
            telegram_membership.stories_per_day = 2
            chat_response = story_freq_message.format(telegram_membership.stories_per_day)
            telegram_membership.save()
        elif text == '/onestory':
            telegram_membership.stories_per_day = 1
            chat_response = story_freq_message.format(telegram_membership.stories_per_day)
            telegram_membership.save()
        elif text == '/nostory':
            telegram_membership.stories_per_day = 0
            chat_response = story_freq_message.format(telegram_membership.stories_per_day)
            telegram_membership.save()
        elif text == '/buy' or telegram_membership.credits_available <= 0:
            if text == '/buy':
                message = buy_message
            else:
                message = telegram_avatar.zero_credits_message
                # check the number of credits available for this membership
            TelegramWebhookView.send_action_buttons(telegram_avatar.telegram_token, chat_id, inline_keyboards, message)
            return HttpResponse('OK')

        if chat_response:
            TelegramWebhookView.send_message(telegram_avatar.telegram_token, chat_id, chat_response)
            return HttpResponse('OK')

        # Getting the conversation History
        encoding = tiktoken.get_encoding('cl100k_base')

        # Make sure the users message is not too long
        if len(encoding.encode(text)) > telegram_avatar.max_input_tokens:
            return

        conversation = telegram_membership.conv_history
        chat_prompt = telegram_avatar.chat_prompt

        # Adding system content for the first time
        if len(conversation) == 0:
            system_message = {'role': 'system', 'content': chat_prompt}
            conversation.append(system_message)

        max_response_tokens = telegram_avatar.max_response_tokens

        # Storing to the conversation History
        conversation.append({'role': 'user', 'content': text})
        conv_history_tokens = num_tokens_from_messages(conversation)

        token_limit = telegram_avatar.max_conv_tokens

        while conv_history_tokens + max_response_tokens >= token_limit:
            del conversation[1]
            conv_history_tokens = num_tokens_from_messages(conversation)

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation,
            max_tokens=max_response_tokens,
            user=str(telegram_user_id),
        )

        # Chat response
        chat_response = response.choices[0].message['content'].strip()

        # reduce the available credits, update conv context
        conversation.append({'role': 'assistant', 'content': chat_response})
        telegram_membership.conv_history = conversation
        telegram_membership.credits_available -= 1
        telegram_membership.total_openai_tokens_consumed += response.usage['total_tokens']
        telegram_membership.save()

        TelegramWebhookView.send_message(telegram_avatar.telegram_token, chat_id, chat_response)

    @staticmethod
    def send_message(token, chat_id, text, parse_mode='Markdown'):
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
        }
        resp = requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data=data)
        print(resp)

    @staticmethod
    def send_chat_action(token, chat_id, action):
        data = {
            'chat_id': chat_id,
            'action': action
        }
        resp = requests.post('https://api.telegram.org/bot' + token + '/sendChatAction', data=data)
        print(resp)

    @staticmethod
    def send_action_buttons(token, chat_id, inlineKeyboard, message):
        data = {
            'text': message,
            'chat_id': chat_id,
            'reply_markup': json.dumps(inlineKeyboard)
        }
        requests.post('https://api.telegram.org/bot' + token + '/sendMessage', data=data)


class PaymentView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_endpoint_secret)
            # Handle the event
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                print(payment_intent)
                PaymentView.payment_succeeded(payment_intent['metadata'])
            else:
                print('Unhandled event type {}'.format(event['type']))
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e)
            raise e

        return HttpResponse(status=200)

    @staticmethod
    def payment_succeeded(metadata): 
        print(metadata)
        chat_id = metadata["chat_id"]
        bot_id = metadata["bot_id"]
        num_credits = metadata["credits"]
        
        # Make sure the telegram bot ID is valid
        telegram_avatar = TelegramAvatar.objects.filter(
            telegram_bot_id=bot_id).first()
        if telegram_avatar is None:
            return False

        # # Make sure the telegram bot ID is valid
        telegram_user = TelegramUser.objects.filter(
            telegram_user_id=chat_id).first()
        if telegram_user is None:
            return False
   
        telegram_membership, created = TelegramMembership.objects.get_or_create(
            telegram_user=telegram_user, telegram_avatar=telegram_avatar)
        telegram_membership.credits_available += int(num_credits)
        telegram_membership.total_credits_purchased += int(num_credits)
        telegram_membership.save()
        
        # Send message to the user after credit increase
        TelegramWebhookView.send_message(telegram_avatar.telegram_token, int(chat_id),
                                         payment_success_message.format(telegram_membership.credits_available))
        return True
