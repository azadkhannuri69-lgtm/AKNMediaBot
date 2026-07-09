from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "AKN Films Web Service is running!"
