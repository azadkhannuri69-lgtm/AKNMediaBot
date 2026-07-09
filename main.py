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
import os

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
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
                    url="https://buy.stripe.com/aFa5kF4IIeOj95d2epfnO01",
                )
            ],
            [
                InlineKeyboardButton(
                    "🥈 اشتراک ۳ ماهه (€6.99)",
                    url="https://buy.stripe.com/3cIaEZdfe35BftBf1bfnO02",
                )
            ],
            [
                InlineKeyboardButton(
                    "🥇 اشتراک ۱۲ ماهه (€19.99)",
                    url="https://buy.stripe.com/6oU6oJ6QQay35T1f1bfnO00",
                )
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "💎 لطفاً اشتراک مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup,
        )

    elif text == "👤 حساب من":
        await update.message.reply_text(
            "👤 هنوز اشتراکی برای این حساب ثبت نشده است."
        )

    elif text == "ℹ️ راهنما":
        await update.message.reply_text(
            "📞 در صورت نیاز با پشتیبانی AKN Media تماس بگیرید."
        )

    else:
        await update.message.reply_text(
            "لطفاً یکی از دکمه‌های منو را انتخاب کنید."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))

print("Bot is running...")
app.run_polling()
