from flask import Blueprint, request
import stripe
from datetime import datetime, timedelta
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, PRICE_1_WEEK, PRICE_1_MONTH, PRICE_3_MONTHS, PRICE_12_MONTHS
from database import save_subscription

webhook = Blueprint("webhook", __name__)
stripe.api_key = STRIPE_SECRET_KEY

@webhook.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except: return "Invalid", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")
        price_id = session.get("line_items", {}).get("data", [{}])[0].get("price", {}).get("id")
        
        # ذخیره در دیتابیس
        save_subscription(int(user_id), "User", "Subscription", session.get("id"), (datetime.utcnow() + timedelta(days=30)).isoformat(), "active")
    return "OK", 200
