from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from telegram.constants import ChatMemberStatus

import logging
from datetime import datetime

from config import (
    TOKEN,
    CHANNEL_ID,
)

from database import (
    init_db,
    get_user,
)

from payments import (
    create_checkout_session,
)

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# -----------------------------
# Database
# -----------------------------

init_db()

# -----------------------------
# Keyboard
# -----------------------------

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ],
    resize_keyboard=True,
)

# -----------------------------
# Check Channel Membership
# -----------------------------

async def is_member(context, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(
            CHANNEL_ID,
            user_id,
        )

        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )

    except Exception as e:
        logger.error(e)
        return False


# -----------------------------
# Start
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    joined = await is_member(
        context,
        user.id,
    )

    if not joined:

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 عضویت در کانال",
                        url="https://t.me/AKNMedia",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ بررسی عضویت",
                        callback_data="check_join",
                    )
                ],
            ]
        )

        await update.message.reply_text(
            "برای استفاده از ربات ابتدا در کانال عضو شوید.",
            reply_markup=keyboard,
        )
        return

    await update.message.reply_text(
        f"سلام {user.first_name} 🌹\n\n"
        "به AKN Media خوش آمدید.\n\n"
        "از منوی زیر گزینه موردنظر را انتخاب کنید.",
        reply_markup=MAIN_KEYBOARD,
    )


# -----------------------------
# Check Join Callback
# -----------------------------

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = await update.callback_query.answer()

    user = update.effective_user

    joined = await is_member(
        context,
        user.id,
    )

    if joined:

        await update.callback_query.message.reply_text(
            "✅ عضویت شما تأیید شد.",
            reply_markup=MAIN_KEYBOARD,
        )

    else:

        await update.callback_query.message.reply_text(
            "❌ هنوز عضو کانال نشده‌اید."
        )
        # -----------------------------
# Buy Subscription
# -----------------------------

async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🗓 ۱ هفته (€0.99)",
                    callback_data="plan_week",
                )
            ],
            [
                InlineKeyboardButton(
                    "🗓 ۱ ماه",
                    callback_data="plan_1m",
                )
            ],
            [
                InlineKeyboardButton(
                    "🗓 ۳ ماه",
                    callback_data="plan_3m",
                )
            ],
            [
                InlineKeyboardButton(
                    "🗓 ۱۲ ماه",
                    callback_data="plan_12m",
                )
            ],
        ]
    )

    await update.message.reply_text(
        "📦 لطفاً پلن اشتراک خود را انتخاب کنید:",
        reply_markup=keyboard,
    )


# -----------------------------
# My Account
# -----------------------------

async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    account = get_user(user.id)

    if account is None:

        await update.message.reply_text(
            "❌ هنوز اشتراکی برای این حساب ثبت نشده است."
        )
        return

    expire = account.get("expires_at", "-")
    status = account.get("status", "Inactive")
    subscription = account.get("subscription", "-")

    await update.message.reply_text(
        f"👤 حساب کاربری\n\n"
        f"🆔 {user.id}\n"
        f"📦 پلن: {subscription}\n"
        f"📅 انقضا: {expire}\n"
        f"✅ وضعیت: {status}"
    )


# -----------------------------
# Help
# -----------------------------

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "ℹ️ راهنما\n\n"
        "• ابتدا در کانال عضو شوید.\n"
        "• پلن موردنظر را خریداری کنید.\n"
        "• پس از پرداخت، اشتراک شما به صورت خودکار فعال می‌شود.\n"
        "• در صورت بروز مشکل با پشتیبانی تماس بگیرید."
    )


# -----------------------------
# Subscription Plans
# -----------------------------

async def subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id

    plans = {
        "plan_week": "week",
        "plan_1m": "month",
        "plan_3m": "3months",
        "plan_12m": "12months",
    }

    if query.data not in plans:
        return

    plan = plans[query.data]

    try:

        checkout_url = create_checkout_session(
            telegram_id=telegram_id,
            plan=plan,
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💳 پرداخت",
                        url=checkout_url,
                    )
                ]
            ]
        )

        await query.message.reply_text(
            "برای تکمیل خرید روی دکمه زیر کلیک کنید.",
            reply_markup=keyboard,
        )

    except Exception as e:

        logger.exception(e)

        await query.message.reply_text(
            "❌ خطا در ایجاد لینک پرداخت."
        )


# -----------------------------
# Main Menu
# -----------------------------

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🎬 خرید اشتراک":
        await buy_subscription(update, context)

    elif text == "👤 حساب من":
        await my_account(update, context)

    elif text == "ℹ️ راهنما":
        await help_menu(update, context)
        # -----------------------------
# Error Handler
# -----------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception("Unhandled exception:", exc_info=context.error)


# -----------------------------
# Register Handlers
# -----------------------------

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu,
    )
)

app.add_handler(
    CallbackQueryHandler(
        check_join,
        pattern="^check_join$",
    )
)

app.add_handler(
    CallbackQueryHandler(
        subscription_callback,
        pattern="^plan_",
    )
)

app.add_error_handler(error_handler)

# -----------------------------
# Startup
# -----------------------------

def main():

    logger.info("====================================")
    logger.info("AKN Media Bot Started")
    logger.info("Python Telegram Bot Running...")
    logger.info("====================================")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    main()
