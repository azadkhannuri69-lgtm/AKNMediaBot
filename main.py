import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus
from config import TOKEN, CHANNEL_ID
from database import init_db, get_user, has_active_subscription
from payments import create_checkout_session

# تنظیم لاگینگ
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# مقداردهی دیتابیس
init_db()

MAIN_KEYBOARD = ReplyKeyboardMarkup([["🎬 خرید اشتراک"], ["👤 حساب من"], ["ℹ️ راهنما"]], resize_keyboard=True)

# توابع منطقی ربات
async def is_member(context, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await is_member(context, user.id):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📢 عضویت", url="https://t.me/AKNMedia")], [InlineKeyboardButton("✅ بررسی", callback_data="check_join")]])
        await update.message.reply_text("برای استفاده ابتدا در کانال عضو شوید.", reply_markup=keyboard)
        return
    await update.message.reply_text(f"سلام {user.first_name}، خوش آمدید.", reply_markup=MAIN_KEYBOARD)

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_member(context, query.from_user.id):
        await query.message.reply_text("✅ تأیید شد.", reply_markup=MAIN_KEYBOARD)
    else:
        await query.answer("❌ هنوز عضو نشده‌اید.", show_alert=True)

async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if has_active_subscription(update.effective_user.id):
        await update.message.reply_text("شما قبلاً اشتراک فعال دارید.")
        return
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗓 ۱ هفته (€0.99)", callback_data="plan_week")],
        [InlineKeyboardButton("🗓 ۱ ماه", callback_data="plan_1m")],
        [InlineKeyboardButton("🗓 ۳ ماه", callback_data="plan_3m")],
        [InlineKeyboardButton("🗓 ۱۲ ماه", callback_data="plan_12m")]
    ])
    await update.message.reply_text("پلن خود را انتخاب کنید:", reply_markup=keyboard)

async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    acc = get_user(user.id)
    if not acc: await update.message.reply_text("اشتراکی ندارید."); return
    await update.message.reply_text(f"👤 پلن: {acc['subscription']}\n📅 انقضا: {acc['expires_at']}\n✅ وضعیت: {acc['status']}")

async def subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    plans = {"plan_week": "week", "plan_1m": "month", "plan_3m": "3months", "plan_12m": "12months"}
    try:
        url = create_checkout_session(plans[query.data], query.from_user.id)
        await query.message.reply_text("برای پرداخت کلیک کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 پرداخت", url=url)]]))
    except Exception as e:
        logger.error(e)
        await query.message.reply_text("خطا در درگاه پرداخت.")

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🎬 خرید اشتراک": await buy_subscription(update, context)
    elif text == "👤 حساب من": await my_account(update, context)
    elif text == "ℹ️ راهنما": await update.message.reply_text("راهنما...")

# بخش اصلی اجرای ربات
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    app.add_handler(CallbackQueryHandler(subscription_callback, pattern="^plan_"))
    
    print("Bot is running...")
    app.run_polling()
