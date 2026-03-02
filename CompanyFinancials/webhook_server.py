from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_DIR = "data/webhook_payloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/webhook/insta", methods=["POST"])
def insta_webhook():
    payload = request.get_json(force=True)

    # Optional: validate API key if Insta sends one
    # api_key = request.headers.get("Authorization")

    timestamp = datetime.utcnow().isoformat()
    file_path = f"{OUTPUT_DIR}/insta_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000)
