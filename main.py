import asyncio

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import (
    TOKEN,
    CHANNEL_ID,
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

from payments import create_checkout_session
from database import cursor


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        member = await context.bot.get_chat_member(
        CHANNEL_ID,
        update.effective_user.id,
    )

    if member.status in ["left", "kicked"]:

        await update.message.reply_text(
            "⚠️ برای استفاده از ربات ابتدا در کانال عضو شوید."
        )

        return

    keyboard = [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        "🎉 به AKN Media خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید.",
        reply_markup=reply_markup,
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🎬 خرید اشتراک":
        cursor.execute(
    """
    SELECT expires_at, status
    FROM users
    WHERE user_id=?
    """,
    (update.effective_user.id,),
)

user = cursor.fetchone()

if user and user[0] and user[1] == "active":

    from datetime import datetime

    if datetime.fromisoformat(user[0]) > datetime.now():

        await update.message.reply_text(
            "✅ شما هم‌اکنون اشتراک فعال دارید.\n\n📅 تا پایان اعتبار، نیازی به خرید مجدد نیست."
        )
        return

        keyboard = [
            [
                InlineKeyboardButton(
                    "🥉 اشتراک ۱ ماهه (€2.99)",
                    url=create_checkout_session(
                        PRICE_1_MONTH,
                        "https://aknmediaweb.onrender.com/success",
                        "https://aknmediaweb.onrender.com/cancel",
                        update.effective_user.id,
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🥈 اشتراک ۳ ماهه (€6.99)",
                    url=create_checkout_session(
                        PRICE_3_MONTHS,
                        "https://aknmediaweb.onrender.com/success",
                        "https://aknmediaweb.onrender.com/cancel",
                        update.effective_user.id,
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🥇 اشتراک ۱۲ ماهه (€19.99)",
                    url=create_checkout_session(
                        PRICE_12_MONTHS,
                        "https://aknmediaweb.onrender.com/success",
                        "https://aknmediaweb.onrender.com/cancel",
                        update.effective_user.id,
                    ),
                )
            ],
        ]

        await update.message.reply_text(
            "💎 لطفاً اشتراک مورد نظر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif text == "👤 حساب من":

        cursor.execute(
            """
            SELECT subscription, expires_at, status
FROM users
WHERE user_id=?
            """,
            (
                update.effective_user.id,
            ),
        )

        user = cursor.fetchone()

        from datetime import datetime

if user:

    status = user[2]

    if user[1]:
        expire_date = datetime.fromisoformat(user[1])

        if expire_date < datetime.now():
            status = "expired"

    await update.message.reply_text(
        f"📦 اشتراک: {user[0]}\n"
        f"📅 اعتبار تا: {user[1]}\n"
        f"📌 وضعیت: {status}"
    )

        else:

            await update.message.reply_text(
                "❌ هنوز اشتراکی برای این حساب ثبت نشده است."
            )

    elif text == "ℹ️ راهنما":

        await update.message.reply_text(
            "📞 برای دریافت پشتیبانی با AKN Media تماس بگیرید."
        )

    else:

        await update.message.reply_text(
            "لطفاً یکی از دکمه‌های منو را انتخاب کنید."
        )


application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu,
    )
)


async def run():

    print("Bot is running...")

    await application.initialize()
    await application.start()

    await application.updater.start_polling(
        drop_pending_updates=True,
    )

    try:
        while True:
            await asyncio.sleep(3600)

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(run())
