from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN


WELCOME_MESSAGES = [
    "🌙 خوش آمدی... امروز یک استوری خاص منتظر توست.",
    "👀 آماده‌ای؟ شاید استوری بعدی حال و هوایت را عوض کند.",
    "🎭 هر تصویر یک داستان دارد، بیا با هم کشفش کنیم.",
    "✨ خوش آمدی، سفر ما از همین‌جا شروع می‌شود.",
    "🤫 بعضی استوری‌ها فقط دیده نمی‌شوند، حس می‌شوند."
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random

    await update.message.reply_text(
        random.choice(WELCOME_MESSAGES)
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
