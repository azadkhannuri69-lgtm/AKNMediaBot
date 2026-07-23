from flask import Flask
from webhook import webhook
from database import init_db

app = Flask(__name__)

# ایجاد دیتابیس هنگام اجرای برنامه
init_db()

# ثبت Webhook
app.register_blueprint(webhook)


@app.route("/")
def home():
    return {
        "status": "online",
        "service": "AKNMediaBot"
    }, 200


@app.route("/success")
def success():
    return "Payment Successful ✅", 200


@app.route("/cancel")
def cancel():
    return "Payment Cancelled ❌", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
