import os
from flask import Flask, request, jsonify

from providers.instafinancials import InstaFinancialsClient

# Flask app object (THIS IS CRITICAL for gunicorn)
app = Flask(__name__)


# Health check (useful for Railway / monitoring)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# Home page
@app.route("/", methods=["GET"])
def home():
    return "Application is running successfully 🚀"


# Example API endpoint
@app.route("/company", methods=["GET"])
def get_company_data():
    cin = request.args.get("cin")

    if not cin:
        return jsonify({"error": "cin parameter is required"}), 400

    client = InstaFinancialsClient()
    data = client.get_company_data(cin)

    # Log for Railway visibility
    print("Order accepted:", data)

    return jsonify(data)


# Local development only
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )