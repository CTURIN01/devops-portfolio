from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "notification-service"}), 200

@app.post("/notify")
def notify():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    message = data.get("message")
    event_type = data.get("event_type", "generic")

    if not user_id or not message:
        return jsonify({
            "status": "error",
            "error": "user_id and message are required"
        }), 400

    return jsonify({
        "status": "sent",
        "service": "notification-service",
        "user_id": user_id,
        "event_type": event_type,
        "message": message
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
