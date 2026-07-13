import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from database import init_db
# سایر ایمپورت‌های مورد نیاز خود (مثل start, menu و...) را اینجا بگذارید

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

if __name__ == "__main__":
    init_db()
    app = Application.builder().token(TOKEN).build()
    
    # هندلرهای خود را اینجا اضافه کنید
    app.add_handler(CommandHandler("start", start))
    # ... بقیه هندلرها ...
    
    print("Bot is running...")
    app.run_polling()
