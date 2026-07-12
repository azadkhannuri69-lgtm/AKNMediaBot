from flask import Flask
from webhook import webhook

app = Flask(__name__)
app.register_blueprint(webhook)

@app.route("/")
def home():
    return "AKN Media Bot is running."

@app.route("/success")
def success():
    return "✅ Payment Successful. You can return to the bot."

@app.route("/cancel")
def cancel():
    return "❌ Payment Cancelled."
