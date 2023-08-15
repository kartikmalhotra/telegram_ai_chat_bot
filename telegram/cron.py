from datetime import datetime

from telegram.models import *
from telegram.config import *
from telegram.views import TelegramWebhookView

import openai

# Set your OpenAI API key
openai.api_key = openai_api_key


def send_story_to_all_memberships():
    print('Running send_story_to_all_memberships')

    avatars = TelegramAvatar.objects.filter()
    for avatar in avatars:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'system', 'content': avatar.story_prompt}],
            max_tokens=avatar.max_response_tokens
        )

        chat_response = response.choices[0].message['content'].strip()

        # get all memberships
        memberships = TelegramMembership.objects.filter(telegram_avatar=avatar)
        for membership in memberships:
            if membership.stories_per_day == 0:
                continue
            elif membership.stories_per_day == 1 and datetime.now().hour < 16:
                continue
            elif membership.stories_per_day == 2 and datetime.now().hour < 11:
                continue

            TelegramWebhookView.send_message(avatar.telegram_token, membership.telegram_user.telegram_user_id,
                                             chat_response)
