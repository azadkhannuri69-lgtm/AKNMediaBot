import asyncio
from datetime import datetime

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
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import (
    TOKEN,
    CHANNEL_ID,
    PRICE_1_WEEK,
    PRICE_1_MONTH,
    PRICE_3_MONTHS,
    PRICE_12_MONTHS,
)

from payments import create_checkout_session
from database import (
    get_user,
    has_active_subscription,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
member = await context.bot.get_chat_member(
    CHANNEL_ID,
    update.effective_user.id,
)

if member.status in ["left", "kicked"]:
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url="https://t.me/AKNMedia",
            )
        ],
        [
            InlineKeyboardButton(
                "✅ بررسی عضویت",
                callback_data="check_membership",
            )
        ],
    ]

    await update.message.reply_text(
        "ابتدا عضو کانال شوید.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return    

    keyboard = [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ]

    await update.message.reply_text(
        "🎉 به AKN Media خوش آمدید.\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
try:
    member = await context.bot.get_chat_member(
        CHANNEL_ID,
        query.from_user.id,
    )
except Exception:
    await query.message.reply_text(
        "❌ خطا در بررسی عضویت."
    )
    return
    
    member = await context.bot.get_chat_member(
        CHANNEL_ID,
        query.from_user.id,
    )

    if member.status in ["left", "kicked"]:
        await query.message.reply_text(
            "❌ هنوز عضو کانال نشده‌اید."
        )
        return

    keyboard = [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ]

    await query.message.reply_text(
        "✅ عضویت شما تأیید شد.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎬 خرید اشتراک":
        if has_active_subscription(update.effective_user.id):
    await update.message.reply_text(
        "✅ شما هم‌اکنون اشتراک فعال دارید."
    )
    return

        keyboard = [
            [
                InlineKeyboardButton(
                    [
    InlineKeyboardButton(
        "⭐ اشتراک ۱ هفته (€0.99)",
        url=create_checkout_session(
            "week",
            update.effective_user.id,
        ),
    )
],
                    "🥉 اشتراک ۱ ماهه (€2.99)",
                    url=create_checkout_session(
                        PRICE_1_MONTH,
                        url=create_checkout_session(
    "month",
    update.effective_user.id,
),
                )
            ],
            [
                InlineKeyboardButton(
                    "🥈 اشتراک ۳ ماهه (€6.99)",
                   url=create_checkout_session(
    "3months",
    update.effective_user.id,
),
                )
            ],
            [
                InlineKeyboardButton(
                    "🥇 اشتراک ۱۲ ماهه (€19.99)",
                   url=create_checkout_session(
    "12months",
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
        user = get_user(update.effective_user.id)

if user:
    await update.message.reply_text(
        f"📦 اشتراک: {user['subscription']}\n"
        f"📅 اعتبار تا: {user['expires_at']}\n"
        f"📌 وضعیت: {user['status']}"
    )
else:
    await update.message.reply_text(
        "❌ هنوز اشتراکی ثبت نشده است."
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
    CallbackQueryHandler(
        check_membership,
        pattern="^check_membership$",
    )
)
application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu,
    )
)
application.add_error_handler(error_handler)

async def error_handler(update, context):
    print(f"❌ Error: {context.error}")
async def run():
    print("Bot is running...")

    await application.initialize()
    await application.bot.delete_webhook(drop_pending_updates=True)
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
