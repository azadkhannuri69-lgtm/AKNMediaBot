import stripe
from config import (
    STRIPE_SECRET_KEY,
    BASE_URL,
    PLANS,
)

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(telegram_id, plan):
    price_id = PLANS.get(plan)

    if not price_id:
        return None

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
        success_url=f"{BASE_URL}/success",
        cancel_url=f"{BASE_URL}/cancel",
    )

    return session.url
