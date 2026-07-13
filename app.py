from flask import Flask
from webhook import webhook

app = Flask(__name__)

app.register_blueprint(webhook)


@app.route("/")
def home():
    return "AKN Media Bot is running."


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
