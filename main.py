import logging
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

from config import TOKEN, CHANNEL_ID
from database import init_db, get_user, has_active_subscription
from payments import create_checkout_session

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

init_db()

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🎬 خرید اشتراک"],
        ["👤 حساب من"],
        ["ℹ️ راهنما"],
    ],
    resize_keyboard=True,
)


async def is_member(context, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception as e:
        logger.error(f"Membership Error: {e}")
        return False
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not await is_member(context, user.id):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 عضویت", url="https://t.me/AKNMedia")],
            [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check_join")]
        ])

        await update.message.reply_text(
            "ابتدا در کانال عضو شوید.",
            reply_markup=keyboard
        )
        return

    await update.message.reply_text(
        f"سلام {user.first_name} 👋",
        reply_markup=MAIN_KEYBOARD
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await is_member(context, query.from_user.id):
        await query.edit_message_text("✅ عضویت تأیید شد.")
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="منوی اصلی:",
            reply_markup=MAIN_KEYBOARD,
        )
    else:
        await query.answer(
            "❌ هنوز عضو کانال نیستید.",
            show_alert=True,
        )
    async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if has_active_subscription(user.id):
        await update.message.reply_text(
            "✅ اشتراک شما فعال است."
        )
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 1 هفته", callback_data="plan_1w")],
        [InlineKeyboardButton("📆 1 ماه", callback_data="plan_1m")],
        [InlineKeyboardButton("🗓 3 ماه", callback_data="plan_3m")],
        [InlineKeyboardButton("📌 12 ماه", callback_data="plan_12m")],
    ])

    await update.message.reply_text(
        "پلن موردنظر را انتخاب کنید:",
        reply_markup=keyboard,
    )


async def subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("plan_", "")

    checkout_url = create_checkout_session(
        telegram_id=query.from_user.id,
        plan=plan,
    )

    if checkout_url:
        await query.edit_message_text(
            f"💳 پرداخت:\n{checkout_url}"
        )
    else:
        await query.edit_message_text(
            "❌ خطا در ایجاد لینک پرداخت."
        )
    async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎬 خرید اشتراک":
        await buy_subscription(update, context)

    elif text == "👤 حساب من":
        await my_account(update, context)

    elif text == "ℹ️ راهنما":
        await update.message.reply_text(
            "ربات AKN Media آماده استفاده است."
        )


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    app.add_handler(CallbackQueryHandler(subscription_callback, pattern="^plan_"))

    print("✅ Bot Started")
    app.run_polling(drop_pending_updates=True)
async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    info = get_user(user.id)

    if not info:
        await update.message.reply_text(
            "❌ اطلاعاتی یافت نشد."
        )
        return

    status = "✅ فعال" if has_active_subscription(user.id) else "❌ غیرفعال"

    text = (
        f"👤 نام: {user.first_name}\n"
        f"🆔 آیدی: {user.id}\n"
        f"📦 وضعیت اشتراک: {status}"
    )

    await update.message.reply_text(text)
