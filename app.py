from flask import Flask
from webhook import webhook

app = Flask(__name__)
app.register_blueprint(webhook)

@app.route("/")
def home(): return "Bot is running."

@app.route("/success")
def success(): return "Payment Successful."

@app.route("/cancel")
def cancel(): return "Payment Cancelled."
