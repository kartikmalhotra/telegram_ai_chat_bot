from ai_chat_bot.settings import ENVIRONMENT, LOCAL, PROD

openai_api_key = '<OPEN_AI_KEY>'

balance_message = '🤖 You have {} credits available'
help_message = '🤖 Response to /help command'
buy_message = '🤖 Please select the credits that you want to purchase'
restart_message = '🤖 Conversation restarted'
payment_message = "🤖 Tap the link below to pay \n" \
                  "[👉 Pay Stripe Invoice]({}) 💳\n\n" \
                  "🔐 We use a trusted payment gateway - Stripe. " \
                  "We do not store your payment data. "
payment_success_message = '🤖 Your payment was successful, you have {} credits available now!\n\n' \
                          'You can use "/balance" command to see your balance at anytime.'
story_freq_message = '🤖 Sure, we will send you {} stories everyday'


if ENVIRONMENT == LOCAL:
    stripe_public_key = "<Stripe public key>"
    stripe_secret_key = "<Stripe secret key>"

    # If you are testing your webhook locally with the Stripe CLI you
    # can find the endpoint's secret by running `stripe listen`
    # Otherwise, find your endpoint's secret in your webhook settings in the Developer Dashboard
    stripe_endpoint_secret ='<Stripe endpoint secret secret>'

    plan_list = [
        {
            "text": "500 credits | 7.99 €",
            'price_id': '<Price_id>',
            'quantity': 1,
            'credits': 550,
            "price": 7.99,
            "callback_data": "<Price_id"
        },
        {
            "text": "250 credits | 3.99 €",
            'price_id': '<Price_id',
            'quantity': 1,
            'credits': 250,
            'price': 3.99,
            "callback_data": "<Price_id"
        },
        {
            "text": "100 credits | 1.99 €",
            'price_id': '<Price_id',
            'quantity': 1,
            'credits': 100,
            'price': 1.99,
            "callback_data": "<Price_id"
        }
    ]
else:
    stripe_public_key = "<Stripe public key>"
    stripe_secret_key = "<Stripe secret key>"

    # If you are testing your webhook locally with the Stripe CLI you
    # can find the endpoint's secret by running `stripe listen`
    # Otherwise, find your endpoint's secret in your webhook settings in the Developer Dashboard
    stripe_endpoint_secret ='<Stripe endpoint secret secret>'

    plan_list = [
        {
            "text": "500 credits | 7.99 €",
            'price_id': '<Price_id>',
            'quantity': 1,
            'credits': 550,
            "price": 7.99,
            "callback_data": '<Price_id>'
        },
        {
            "text": "250 credits | 3.99 €",
            'price_id': '<Price_id>',
            'quantity': 1,
            'credits': 250,
            'price': 3.99,
            "callback_data": '<Price_id>'
        },
        {
            "text": "100 credits | 1.99 €",
            'price_id': '<Price_id>',
            'quantity': 1,
            'credits': 100,
            'price': 1.99,
            "callback_data": '<Price_id>'
        }
    ]

inline_keyboards = {
    "inline_keyboard": [
        [plan_list[0]],
        [plan_list[1]],
        [plan_list[2]]
    ]
}
