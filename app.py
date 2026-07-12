from flask import Flask
from webhook import webhook

app = Flask(__name__)
app.register_blueprint(webhook)

@app.route("/")
def home():
    return "AKN Media Bot Webhook Server is running."
