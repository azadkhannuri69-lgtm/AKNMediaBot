import os

# =========================
# Telegram
# =========================
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@AKNMedia")

# =========================
# Database
# =========================
DATABASE_NAME = os.getenv("DATABASE_NAME", "database.db")

# =========================
# Render / Website
# =========================
BASE_URL = os.getenv("BASE_URL")

# =========================
# Stripe
# =========================
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# =========================
# Stripe Price IDs
# =========================
PRICE_1_WEEK = os.getenv("PRICE_1_WEEK")
PRICE_1_MONTH = os.getenv("PRICE_1_MONTH")
PRICE_3_MONTHS = os.getenv("PRICE_3_MONTHS")
PRICE_12_MONTHS = os.getenv("PRICE_12_MONTHS")

# =========================
# Subscription Plans
# =========================
PLANS = {
    PRICE_1_WEEK: {
        "name": "1 Week",
        "days": 7,
        "price": "€0.99",
    },
    PRICE_1_MONTH: {
        "name": "1 Month",
        "days": 30,
        "price": "Monthly",
    },
    PRICE_3_MONTHS: {
        "name": "3 Months",
        "days": 90,
        "price": "Quarterly",
    },
    PRICE_12_MONTHS: {
        "name": "12 Months",
        "days": 365,
        "price": "Yearly",
    },
}
