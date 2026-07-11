from flask import Blueprint, request, jsonify
import stripe

from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
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

        plan = "Unknown"

        metadata = session.get("metadata")

        if metadata:
            plan = metadata.get("plan", "Unknown")

        cursor.execute(
            """
            INSERT OR REPLACE INTO users
            (
                user_id,
                subscription,
                payment_id,
                status
            )
            VALUES
            (
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
                "active",
            ),
        )

            conn.commit()

    import requests
    from config import TOKEN

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": telegram_id,
            "text": "✅ پرداخت شما با موفقیت انجام شد.\n\n🎉 اشتراک شما فعال شد.\n\nاز AKN Media سپاسگزاریم.",
        },
    )

    print(f"Subscription Activated: {telegram_id}")

    return jsonify({"received": True}), 200
