from flask import Blueprint, request, jsonify

webhook = Blueprint("webhook", __name__)

@webhook.route("/webhook", methods=["POST"])
def stripe_webhook():
    event = request.get_json()

    print(event)

    return jsonify({"received": True}), 200
