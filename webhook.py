from flask import Blueprint, request, jsonify
import stripe
import asyncio

from telegram import Bot

from config import (
    TOKEN,
    CHANNEL_ID,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
)

from database import conn, cursor

stripe.api_key = STRIPE_SECRET_KEY

bot = Bot(TOKEN)

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

    except Exception as e:
        print(e)
        return jsonify({"success": False}), 400

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        telegram_id = int(session["client_reference_id"])
        plan = session["metadata"]["plan"]
        payment_id = session["id"]

        cursor.execute(
            """
            INSERT OR REPLACE INTO users
            (user_id, plan, payment_id, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                telegram_id,
                plan,
                payment_id,
                "active",
            ),
        )

        conn.commit()

        async def send_invite():

            invite = await bot.create_chat_invite_link(
                chat_id=CHANNEL_ID,
                member_limit=1,
                creates_join_request=False,
            )

            await bot.send_message(
                chat_id=telegram_id,
                text=(
                    "✅ پرداخت شما با موفقیت انجام شد.\n\n"
                    "برای ورود به کانال از لینک زیر استفاده کنید:\n\n"
                    f"{invite.invite_link}"
                ),
            )

        asyncio.run(send_invite())

    return jsonify({"received": True}), 200
