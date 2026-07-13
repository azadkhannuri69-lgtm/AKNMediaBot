import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@AKNMedia")

DATABASE_NAME = os.getenv("DATABASE_NAME", "database.db")

BASE_URL = os.getenv("BASE_URL")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

PRICE_1_WEEK = os.getenv("PRICE_1_WEEK")
PRICE_1_MONTH = os.getenv("PRICE_1_MONTH")
PRICE_3_MONTHS = os.getenv("PRICE_3_MONTHS")
PRICE_12_MONTHS = os.getenv("PRICE_12_MONTHS")

PLANS = {
    "1w": PRICE_1_WEEK,
    "1m": PRICE_1_MONTH,
    "3m": PRICE_3_MONTHS,
    "12m": PRICE_12_MONTHS,
}
