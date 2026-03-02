from .nse_client import NSEClient
from .filters import filter_annual_reports

nse = NSEClient()

def process_company(symbol):
    announcements = nse.fetch_announcements(symbol)
    reports = filter_annual_reports(announcements)

    return reports