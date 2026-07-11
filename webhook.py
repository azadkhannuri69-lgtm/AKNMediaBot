from flask import Blueprint, request, jsonify
import stripe
import requests
from datetime import datetime, timedelta

from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, TOKEN
from database import cursor, conn

stripe.api_key = STRIPE_SECRET_KEY

webhook = Blueprint("webhook", __name__)


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

    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400

    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        telegram_id = int(session.get("client_reference_id"))
        payment_id = session.get("id")

        metadata = session.get("metadata", {})
        plan = metadata.get("plan", "Unknown")

        if plan == "price_1Tr1njQ4IuPkYuATjSUy4CEz":
            expires_at = datetime.now() + timedelta(days=30)

        elif plan == "price_1Tr1u9Q4IuPkYuATujbQGPwX":
            expires_at = datetime.now() + timedelta(days=90)

        elif plan == "price_1Tr21JQ4IuPkYuATCbM9T1Z6":
            expires_at = datetime.now() + timedelta(days=365)

        else:
            expires_at = datetime.now()

        cursor.execute(
            """
            INSERT OR REPLACE INTO users
            (
                user_id,
                subscription,
                payment_id,
                expires_at,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                telegram_id,
                plan,
                payment_id,
                expires_at.isoformat(),
                "active",
            ),
        )

        conn.commit()

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": telegram_id,
                "text": "✅ پرداخت شما با موفقیت انجام شد.\n\n🎉 اشتراک شما فعال شد.\n\nاز AKN Media سپاسگزاریم.",
            },
        )

        print(f"Subscription Activated: {telegram_id}")

    return jsonify({"received": True}), 200
