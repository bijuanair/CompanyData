# -------------------------------------------------
# app.py  (Flask Web UI for InstaFinancials)
# -------------------------------------------------

print(">>> app.py started")

import os
import sys
import yaml
from flask import Flask, render_template, request

# -------------------------------------------------
# Resolve project root & fix Python path
# -------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# -------------------------------------------------
# Load config.yaml from project root
# -------------------------------------------------
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# -------------------------------------------------
# Imports AFTER path setup
# -------------------------------------------------
from providers.instafinancials import InstaFinancialsClient

INSTA_API_KEY = config["insta"]["api_key"]
BASE_URL = config["insta"]["base_url"]
WEBHOOK_URL = config["insta"]["webhook_url"]

# -------------------------------------------------
# Helper: flatten nested JSON for table display
# -------------------------------------------------

def flatten_json(data, parent_key="", sep=".", strip_prefixes=None):
    """
    Flattens nested JSON and removes provider-specific prefixes
    """
    if strip_prefixes is None:
        strip_prefixes = ["InstaBasic", "InstaFinancials"]

    items = []

    for k, v in data.items():
        # Remove known provider prefixes
        clean_key = k
        for prefix in strip_prefixes:
            if clean_key.startswith(prefix + sep):
                clean_key = clean_key[len(prefix) + 1:]
            elif clean_key == prefix:
                clean_key = ""

        new_key = f"{parent_key}{sep}{clean_key}" if parent_key and clean_key else clean_key or parent_key

        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep, strip_prefixes))
        elif isinstance(v, list):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))

    return items

#def flatten_json(data, parent_key="", sep="."):
#    items = []
#    for k, v in data.items():
#        new_key = f"{parent_key}{sep}{k}" if parent_key else k
#        if isinstance(v, dict):
#            items.extend(flatten_json(v, new_key, sep))
#        elif isinstance(v, list):
#            items.append((new_key, str(v)))
#        else:
#            items.append((new_key, v))
#    return items

def group_by_section(flat_items):
    """
    Groups flattened JSON items into logical sections.
    Example:
    CompanyMasterSummary.*
    DirectorSignatoryMasterBasic.DirectorCurrentMasterBasic.*
    """
    sections = {}

    for key, value in flat_items:
        if "." in key:
            section, subkey = key.split(".", 1)
        else:
            section = "General"
            subkey = key

        if section not in sections:
            sections[section] = []

        sections[section].append((subkey, value))

    return sections


# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)

client = InstaFinancialsClient(
    api_key=INSTA_API_KEY,
    base_url=BASE_URL
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    flat_result = None
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
                result = response
                flat_items = flatten_json(response)
                grouped_result = group_by_section(flat_items)


            except Exception as e:
                error = str(e)

    return render_template(
    "index.html",
    result=result,
    grouped_result=grouped_result,
    error=error
)


# -------------------------------------------------
# Start Flask server (DO NOT MODIFY THIS BLOCK)
# -------------------------------------------------
if __name__ == "__main__":
    print(">>> starting flask server")
    app.run(
        host=config["app"]["host"],
        port=config["app"]["port"],
        debug=True
    )
