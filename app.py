from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/healthz/live")
def healthLive():
    return jsonify(status="ok")


@app.route("/healthz/ready")
def healthReady():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
