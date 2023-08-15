import stripe

from ai_chat_bot.settings import DOMAIN

from telegram.config import *


def create_checkout_session(price_id, chat_id, bot_id):
    print("creating checkout session")
    
    plan = None
    for plan in plan_list:
        if plan['price_id'] == price_id:
            break

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                }],
            # client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url=DOMAIN + "/static/payment_success.html",
            cancel_url=DOMAIN + "/static/payment_failed.html",
            payment_method_types=['card'],
            mode='payment',
            currency="eur",
            payment_intent_data={
                'metadata': {
                    'order_id': price_id,
                    "chat_id": chat_id,
                    "bot_id": bot_id,
                    "credits":  plan["credits"]
                }
            },
            allow_promotion_codes=True
        )
        return checkout_session['url']
    except Exception as e:
        print(e)
        return None


