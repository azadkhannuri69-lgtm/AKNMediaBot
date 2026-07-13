from flask import Blueprint, request

import stripe
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from database import save_subscription

webhook = Blueprint("webhook", __name__)

stripe.api_key = STRIPE_SECRET_KEY


@webhook.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return "Invalid webhook", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        telegram_id = int(session["client_reference_id"])
        payment_id = session["id"]

        price_id = session["line_items"]["data"][0]["price"]["id"] if "line_items" in session else ""

        if price_id:
            if price_id == "PRICE_1_WEEK":
                subscription = "1 Week"
            elif price_id == "PRICE_1_MONTH":
                subscription = "1 Month"
            elif price_id == "PRICE_3_MONTHS":
                subscription = "3 Months"
            else:
                subscription = "12 Months"
        else:
            subscription = "Unknown"

        expires_at = session.get("expires_at", "")

        save_subscription(
            user_id=telegram_id,
            username="",
            subscription=subscription,
            payment_id=payment_id,
            expires_at=str(expires_at),
            status="active",
        )

    return "OK", 200
