import stripe

from config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(
    price_id,
    success_url,
    cancel_url,
    telegram_id,
):

    session = stripe.checkout.Session.create(
        mode="subscription",

        payment_method_types=[
            "card",
        ],

        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],

        success_url=success_url,

        cancel_url=cancel_url,

        client_reference_id=str(telegram_id),

        metadata={
            "telegram_id": str(telegram_id),
            "plan": price_id,
        },
    )

    return session.url
