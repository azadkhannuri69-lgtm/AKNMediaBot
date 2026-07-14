import logging

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import TOKEN
from payments import create_checkout_session

logging.basicConfig(level=logging.INFO)

application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🥉 اشتراک ۱ هفته (€0.99)",
                callback_data="week",
            )
        ],
        [
            InlineKeyboardButton(
                "🥈 اشتراک ۱ ماه (€2.99)",
                callback_data="month",
            )
        ],
        [
            InlineKeyboardButton(
                "🥇 اشتراک ۳ ماه (€6.99)",
                callback_data="3months",
            )
        ],
        [
            InlineKeyboardButton(
                "💎 اشتراک ۱۲ ماه (€19.99)",
                callback_data="12months",
            )
        ],
    ]

    await update.message.reply_text(
        "🎬 اشتراک مورد نظر را انتخاب کنید.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data

    payment_url = create_checkout_session(
        plan,
        query.from_user.id,
    )

    await query.message.reply_text(
        "💳 برای پرداخت روی دکمه زیر بزنید.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "پرداخت اشتراک",
                        url=payment_url,
                    )
                ]
            ]
        ),
    )


application.add_handler(
    CommandHandler(
        "start",
        start,
    )
)

application.add_handler(
    CallbackQueryHandler(
        select_plan,
    )
)

if __name__ == "__main__":
    print("AKN Media Bot Started")

    application.run_polling(
        drop_pending_updates=True,
    )
