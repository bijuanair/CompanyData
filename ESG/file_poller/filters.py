# file_poller/filters.py

from datetime import datetime
from typing import List, Dict


def get_current_fy() -> str:
    """
    Returns current Indian financial year in format: YYYY-YYYY
    Example: 2025-2026
    """
    today = datetime.today()

    if today.month >= 4:
        return f"{today.year}-{today.year + 1}"
    else:
        return f"{today.year - 1}-{today.year}"


def filter_annual_reports(announcements: List[Dict]) -> List[Dict]:
    """
    Filters announcements for:
    - Annual Report
    - Current FY
    """

    current_fy = get_current_fy()
    filtered_reports = []

    for item in announcements:

        subject = item.get("subject", "")
        attachment = item.get("attchmntFile", "")
        date = item.get("anndate", None)

        # Basic filters
        if not subject:
            continue

        if "Annual Report" in subject and current_fy in subject:

            filtered_reports.append({
                "symbol": item.get("symbol"),
                "filing_type": "Annual Report",
                "filing_date": date,
                "financial_year": current_fy,
                "announcement_subject": subject,
                "source_url": attachment
            })

    return filtered_reports