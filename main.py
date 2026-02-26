import os
from flask import Flask, request, render_template, jsonify
from providers.instafinancials import InstaFinancialsClient

app = Flask(__name__, template_folder="web/templates")


@app.route("/", methods=["GET", "POST"])
def index():
    cin = None
    data = None
    error = None

    if request.method == "POST":
        cin = request.form.get("cin", "").strip()

        if not cin:
            error = "CIN is required"
        else:
            try:
                api_key = os.environ.get("INSTA_API_KEY")
                if not api_key:
                    raise Exception("INSTA_API_KEY is not configured")

                client = InstaFinancialsClient(api_key)
                data = client.get_company_data(cin)

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        cin=cin,
        data=data,
        error=error
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )