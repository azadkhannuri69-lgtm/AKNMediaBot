from flask import Blueprint, request
import stripe
from datetime import datetime, timedelta

from config import (
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    PRICE_1_WEEK,
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

from database import save_subscription

webhook = Blueprint("webhook", __name__)

stripe.api_key = STRIPE_SECRET_KEY


@webhook.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    signature = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        return "Invalid Webhook", 400

    if event["type"] != "checkout.session.completed":
        return "OK", 200

    session = event["data"]["object"]

    session = stripe.checkout.Session.retrieve(
        session["id"],
        expand=[
            "line_items",
            "subscription",
            "customer",
        ],
    )

    try:
        user_id = int(session["client_reference_id"])
    except Exception:
        return "Missing Telegram ID", 400

    username = ""

    customer_details = session.get("customer_details")
    if customer_details:
        username = customer_details.get("name", "")

    subscription_id = session.get("subscription", "")

    price_id = session["line_items"]["data"][0]["price"]["id"]

    if price_id == PRICE_1_WEEK:
        subscription = "1 Week"
        expires_at = datetime.utcnow() + timedelta(days=7)

    elif price_id == PRICE_1_MONTH:
        subscription = "1 Month"
        expires_at = datetime.utcnow() + timedelta(days=30)

    elif price_id == PRICE_3_MONTHS:
        subscription = "3 Months"
        expires_at = datetime.utcnow() + timedelta(days=90)

    elif price_id == PRICE_12_MONTHS:
        subscription = "12 Months"
        expires_at = datetime.utcnow() + timedelta(days=365)

    else:
        return "Unknown Price ID", 400

    save_subscription(
        user_id=user_id,
        username=username,
        subscription=subscription,
        payment_id=subscription_id,
        expires_at=expires_at.isoformat(),
        status="active",
    )

    return "OK", 200
