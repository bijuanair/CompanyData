# -------------------------------------------------
# Flask Web App – Railway + Local Compatible
# -------------------------------------------------

import os
import sys
import yaml
from flask import Flask, render_template, request, jsonify

print(">>> app.py started")

# -------------------------------------------------
# Resolve project root (for local dev only)
# -------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# -------------------------------------------------
# Load config.yaml (LOCAL fallback only)
# -------------------------------------------------
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

local_config = {}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        local_config = yaml.safe_load(f)

# -------------------------------------------------
# Environment Variables (Railway)
# -------------------------------------------------
INSTA_API_KEY = os.environ.get(
    "INSTA_API_KEY",
    local_config.get("insta", {}).get("api_key")
)

WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL",
    local_config.get("insta", {}).get("webhook_url")
)

BASE_URL = local_config.get("insta", {}).get(
    "base_url",
    "https://instafinancials.com/api/InstaBasic/v1/json"
)

# -------------------------------------------------
# Import Insta client
# -------------------------------------------------
from providers.instafinancials import InstaFinancialsClient

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def flatten_json(data, parent_key="", sep="."):
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep))
        elif isinstance(v, list):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return items


def group_by_section(flat_items):
    sections = {}
    for key, value in flat_items:
        if "." in key:
            section, subkey = key.split(".", 1)
        else:
            section = "General"
            subkey = key

        if section not in sections:
            sections[section] = {}

        if section == "DirectorSignatoryMasterBasic":
            if subkey.startswith("DirectorCurrentMasterBasic"):
                sub_section = "Current Directors"
            elif subkey.startswith("DirectorPastMasterBasic"):
                sub_section = "Past Directors"
            else:
                sub_section = "Other"

            sections[section].setdefault(sub_section, []).append((subkey, value))
        else:
            sections[section].setdefault("Main", []).append((subkey, value))

    return sections


def extract_summary(flat_items):
    summary_keys = [
        "Response.Status",
        "Response.RequestId",
        "CompanyMasterSummary.CompanyStatus",
        "CompanyMasterSummary.LastUpdatedDateTime"
    ]

    summary = {}
    for key, value in flat_items:
        if key in summary_keys:
            summary[key.split(".")[-1]] = value

    return summary


# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)

client = InstaFinancialsClient(
    api_key=INSTA_API_KEY,
    base_url=BASE_URL
)

# -------------------------------------------------
# Main UI Route
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    grouped_result = None
    summary_data = None
    error = None

    if request.method == "POST":
        cin = request.form.get("cin", "").strip()

        if not cin:
            error = "CIN is required"
        else:
            try:
                response = client.fetch_company_data(
                    lookup_type="CompanyCIN",
                    lookup_value=cin,
                    scope="All",
                    webhook_url=WEBHOOK_URL
                )

                flat_items = flatten_json(response)
                grouped_result = group_by_section(flat_items)
                summary_data = extract_summary(flat_items)

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        grouped_result=grouped_result,
        summary_data=summary_data,
        error=error
    )

# -------------------------------------------------
# Webhook Endpoint (CRITICAL for Railway)
# -------------------------------------------------
@app.route("/webhook/insta", methods=["POST"])
def insta_webhook():
    data = request.json
    print(">>> Webhook received:", data)
    return jsonify({"status": "ok"}), 200


# -------------------------------------------------
# Run App (Railway Compatible)
# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f">>> Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)

# # -------------------------------------------------
# # app.py  (Flask Web UI for InstaFinancials)
# # -------------------------------------------------

# print(">>> app.py started")

# import os
# import sys
# import yaml
# from flask import Flask, render_template, request

# # -------------------------------------------------
# # Resolve project root & fix Python path
# # -------------------------------------------------
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(BASE_DIR)

# # -------------------------------------------------
# # Load config.yaml from project root
# # -------------------------------------------------
# CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# with open(CONFIG_PATH, "r") as f:
#     config = yaml.safe_load(f)

# # -------------------------------------------------
# # Imports AFTER path setup
# # -------------------------------------------------
# from providers.instafinancials import InstaFinancialsClient

# INSTA_API_KEY = config["insta"]["api_key"]
# BASE_URL = config["insta"]["base_url"]
# WEBHOOK_URL = config["insta"]["webhook_url"]

# # -------------------------------------------------
# # Helper: flatten nested JSON for table display
# # -------------------------------------------------

# def flatten_json(data, parent_key="", sep=".", strip_prefixes=None):
#     """
#     Flattens nested JSON and removes provider-specific prefixes
#     """
#     if strip_prefixes is None:
#         strip_prefixes = ["InstaBasic", "InstaFinancials"]

#     items = []

#     for k, v in data.items():
#         # Remove known provider prefixes
#         clean_key = k
#         for prefix in strip_prefixes:
#             if clean_key.startswith(prefix + sep):
#                 clean_key = clean_key[len(prefix) + 1:]
#             elif clean_key == prefix:
#                 clean_key = ""

#         new_key = f"{parent_key}{sep}{clean_key}" if parent_key and clean_key else clean_key or parent_key

#         if isinstance(v, dict):
#             items.extend(flatten_json(v, new_key, sep, strip_prefixes))
#         elif isinstance(v, list):
#             items.append((new_key, str(v)))
#         else:
#             items.append((new_key, v))

#     return items

# #def flatten_json(data, parent_key="", sep="."):
# #    items = []
# #    for k, v in data.items():
# #        new_key = f"{parent_key}{sep}{k}" if parent_key else k
# #        if isinstance(v, dict):
# #            items.extend(flatten_json(v, new_key, sep))
# #        elif isinstance(v, list):
# #            items.append((new_key, str(v)))
# #        else:
# #            items.append((new_key, v))
# #    return items

# def group_by_section(flat_items):
#     sections = {}

#     for key, value in flat_items:
#         if "." in key:
#             section, subkey = key.split(".", 1)
#         else:
#             section = "General"
#             subkey = key

#         if section not in sections:
#             sections[section] = {}

#         # Special handling for Director section
#         if section == "DirectorSignatoryMasterBasic":
#             if subkey.startswith("DirectorCurrentMasterBasic"):
#                 sub_section = "Current Directors"
#             elif subkey.startswith("DirectorPastMasterBasic"):
#                 sub_section = "Past Directors"
#             else:
#                 sub_section = "Other"

#             sections[section].setdefault(sub_section, []).append((subkey, value))
#         else:
#             sections[section].setdefault("Main", []).append((subkey, value))

#     return sections


# # -------------------------------------------------
# # Flask App
# # -------------------------------------------------
# app = Flask(__name__)

# client = InstaFinancialsClient(
#     api_key=INSTA_API_KEY,
#     base_url=BASE_URL
# )

# @app.route("/", methods=["GET", "POST"])
# def index():

#     grouped_result = None
#     summary_data = None
#     error = None

#     if request.method == "POST":
#         cin = request.form.get("cin", "").strip()

#         if not cin:
#             error = "CIN is required"
#         else:
#             try:
#                 response = client.fetch_company_data(
#                     lookup_type="CompanyCIN",
#                     lookup_value=cin,
#                     scope="All",
#                     webhook_url=WEBHOOK_URL
#                 )

#                 flat_items = flatten_json(response)
#                 grouped_result = group_by_section(flat_items)
#                 summary_data = extract_summary(flat_items)

#             except Exception as e:
#                 error = str(e)

#     return render_template(
#         "index.html",
#         grouped_result=grouped_result,
#         summary_data=summary_data,
#         error=error
#     )

# def extract_summary(flat_items):
#     """
#     Extract key fields for summary cards
#     """
#     summary_keys = [
#         "Response.Status",
#         "Response.RequestId",
#         "CompanyMasterSummary.CompanyStatus",
#         "CompanyMasterSummary.LastUpdatedDateTime"
#     ]

#     summary = {}

#     for key, value in flat_items:
#         if key in summary_keys:
#             summary[key.split(".")[-1]] = value

#     return summary

# # -------------------------------------------------
# # Start Flask server (DO NOT MODIFY THIS BLOCK)
# # -------------------------------------------------
# if __name__ == "__main__":
#     print(">>> starting flask server")
#     app.run(
#         host=config["app"]["host"],
#         port=config["app"]["port"],
#         debug=True
#     )
