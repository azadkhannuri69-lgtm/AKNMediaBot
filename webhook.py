from flask import Blueprint, request

import stripe
from datetime import datetime, timedelta

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
            STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return "Invalid webhook", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = int(session["client_reference_id"])
        payment_id = session["payment_intent"]

        price_id = session["line_items"]["data"][0]["price"]["id"] if "line_items" in session else ""

        if price_id == "PRICE_1_WEEK":
            plan = "1 Week"
            expires = datetime.utcnow() + timedelta(days=7)

        elif price_id == "PRICE_1_MONTH":
            plan = "1 Month"
            expires = datetime.utcnow() + timedelta(days=30)

        elif price_id == "PRICE_3_MONTHS":
            plan = "3 Months"
            expires = datetime.utcnow() + timedelta(days=90)

        else:
            plan = "12 Months"
            expires = datetime.utcnow() + timedelta(days=365)

        save_subscription(
            user_id=user_id,
            username="",
            subscription=plan,
            payment_id=payment_id,
            expires_at=expires.isoformat()
        )

    return "OK", 200
