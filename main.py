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
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

from payments import create_checkout_session
from database import cursor


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
            SELECT subscription, status
            FROM users
            WHERE user_id=?
            """,
            (
                update.effective_user.id,
            ),
        )

        user = cursor.fetchone()

        if user:

            await update.message.reply_text(
                f"📦 اشتراک: {user[0]}\n"
                f"📌 وضعیت: {user[1]}"
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
