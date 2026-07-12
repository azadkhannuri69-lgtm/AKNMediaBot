import stripe

from config import (
    STRIPE_SECRET_KEY,
    BASE_URL,
)

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(price_id, telegram_id):
    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        client_reference_id=str(telegram_id),
        metadata={
            "telegram_id": str(telegram_id),
            "price_id": price_id,
        },
        success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/cancel",
        allow_promotion_codes=True,
    )

    return session.url
