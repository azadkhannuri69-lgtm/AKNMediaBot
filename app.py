from flask import Flask
from webhook import webhook
from database import init_db

app = Flask(__name__)

# Initialize SQLite
init_db()

# Register Stripe Webhook
app.register_blueprint(webhook, url_prefix="/")

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "AKNMediaBot",
        "webhook": "/webhook"
    }, 200


@app.get("/success")
def success():
    return "Payment Successful ✅", 200


@app.get("/cancel")
def cancel():
    return "Payment Cancelled ❌", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
