import logging
import stripe

from config import (
    STRIPE_SECRET_KEY,
    BASE_URL,
    PRICE_1_WEEK,
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

logging.basicConfig(level=logging.INFO)

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(plan, telegram_id):
    prices = {
        "week": PRICE_1_WEEK,
        "month": PRICE_1_MONTH,
        "3months": PRICE_3_MONTHS,
        "12months": PRICE_12_MONTHS,
    }

    if plan not in prices:
        raise ValueError(f"Unknown plan: {plan}")

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price": prices[plan],
                    "quantity": 1,
                }
            ],
            client_reference_id=str(telegram_id),
            metadata={
                "plan": plan,
            },
            success_url=f"{BASE_URL}/success",
            cancel_url=f"{BASE_URL}/cancel",
        )

        return session.url

    except Exception as e:
        logging.exception("Stripe Checkout Error")
        raise e
