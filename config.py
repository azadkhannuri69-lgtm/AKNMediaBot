import os

# Telegram
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Price IDs
PRICE_1_WEEK = os.getenv("PRICE_1_WEEK")
PRICE_1_MONTH = os.getenv("PRICE_1_MONTH")
PRICE_3_MONTHS = os.getenv("PRICE_3_MONTHS")
PRICE_12_MONTHS = os.getenv("PRICE_12_MONTHS")

# Website
BASE_URL = os.getenv("BASE_URL")

# Database
DATABASE_NAME = "database.db"
