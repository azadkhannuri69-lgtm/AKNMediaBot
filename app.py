from flask import Flask

from webhook import webhook

app = Flask(__name__)

app.register_blueprint(webhook)


@app.route("/")
def home():
    return "AKN Media Webhook is Running"


@app.route("/success")
def success():
    return (
        "✅ Payment successful."
        "<br><br>"
        "You can now return to Telegram."
    )


@app.route("/cancel")
def cancel():
    return (
        "❌ Payment cancelled."
        "<br><br>"
        "Return to Telegram and try again."
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
    )
