# file_poller/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# Database
# ==============================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/CompanyData"
)

# ==============================
# Poller Settings
# ==============================

POLL_DELAY_SECONDS = 1          # Delay between NSE calls
ANNOUNCEMENT_TYPE = "Annual Report"
EXCHANGE = "NSE"

# ==============================
# Logging
# ==============================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")