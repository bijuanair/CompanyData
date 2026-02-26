import os
from flask import Flask, request, render_template, jsonify
from providers.instafinancials import InstaFinancialsClient

# You chose Option B → templates live under web/templates
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
                # Read API key from environment (Railway variable)
                api_key = os.environ.get("INSTA_API_KEY")
                if not api_key:
                    raise Exception("INSTA_API_KEY is not configured")

                # Instantiate Insta client
                client = InstaFinancialsClient(api_key)

                # ✅ CORRECT METHOD + CORRECT PARAMS
                data = client.fetch_company_data(
                    lookup_type="CompanyCIN",
                    lookup_value=cin,
                    scope="All"
                )

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