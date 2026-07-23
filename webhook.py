from flask import Blueprint, request
import stripe
from telegram import Bot
from datetime import datetime, timedelta

from config import (
    TOKEN,
    CHANNEL_ID,
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
bot = Bot(TOKEN)


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
        expand=["line_items"],
    )

    user_id = int(session["client_reference_id"])

    payment_id = session.get("payment_intent", "")

    username = session.get("customer_details", {}).get("name", "")

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
        return "Unknown Plan", 400

    save_subscription(
        user_id=user_id,
        username=username,
        subscription=subscription,
        payment_id=payment_id,
        expires_at=expires_at.isoformat(),
    )

    try:
        invite = bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )

        bot.send_message(
            chat_id=user_id,
            text=(
                "✅ پرداخت شما با موفقیت انجام شد.\n\n"
                f"📦 اشتراک: {subscription}\n"
                f"📅 پایان: {expires_at.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
                f"🔗 لینک اختصاصی ورود:\n{invite.invite_link}"
            ),
        )

    except Exception as e:
        print(e)

    return "OK", 200
