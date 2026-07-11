from flask import Flask
from webhook import webhook

app = Flask(__name__)

app.register_blueprint(webhook)


@app.route("/")
def home():
    return "AKN Media Web Service is running!"


@app.route("/success")
def success():
    return "Payment Successful"


@app.route("/cancel")
def cancel():
    return "Payment Cancelled"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
