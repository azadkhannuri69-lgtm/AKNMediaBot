from flask import Flask

from webhook import webhook

app = Flask(__name__)

app.register_blueprint(webhook)


@app.route("/")
def home():
    return "AKN Media Bot is running."


@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "AKNMediaBot"
    }, 200


@app.route("/success")
def success():
    return """
    <h2>✅ Payment Successful</h2>
    <p>You can now return to Telegram and use the bot.</p>
    """, 200


@app.route("/cancel")
def cancel():
    return """
    <h2>❌ Payment Cancelled</h2>
    <p>No payment has been made.</p>
    """, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
