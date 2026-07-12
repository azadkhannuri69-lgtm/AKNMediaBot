import stripe

from config import (
    STRIPE_SECRET_KEY,
    BASE_URL,
    PRICE_1_WEEK,
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

stripe.api_key = STRIPE_SECRET_KEY

PRICE_IDS = {
    "week": PRICE_1_WEEK,
    "month": PRICE_1_MONTH,
    "3months": PRICE_3_MONTHS,
    "12months": PRICE_12_MONTHS,
}


def create_checkout_session(plan: str, telegram_id: int):

    if plan not in PRICE_IDS:
        raise ValueError("Invalid subscription plan.")

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[
            {
                "price": PRICE_IDS[plan],
                "quantity": 1,
            }
        ],
        success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/cancel",
        client_reference_id=str(telegram_id),
        allow_promotion_codes=True,
    )

    return session.url
