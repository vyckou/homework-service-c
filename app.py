import threading

from flask import Flask, jsonify

app = Flask(__name__)
health_app = Flask(__name__ + ".health")


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/healthz/live")
@health_app.route("/healthz/live")
def healthLive():
    return jsonify(status="ok")


@app.route("/healthz/ready")
@health_app.route("/healthz/ready")
def healthReady():
    return jsonify(status="ok")


if __name__ == "__main__":
    threading.Thread(
        target=lambda: health_app.run(host="0.0.0.0", port=3000),
        daemon=True,
    ).start()
    app.run(host="0.0.0.0", port=8080)
