# pipeline/fetch_pipeline.py

from typing import Dict
from providers.instafinancials import InstaFinancialsClient

def fetch_company_by_cin(
    client: InstaFinancialsClient,
    cin: str
) -> Dict:
    """
    Fetch full company data using CompanyCIN lookup
    """
    response = client.fetch_company_data(
        lookup_type="CompanyCIN",
        lookup_value=cin,
        scope="All"
    )

    return {
        "cin": cin,
        "raw_response": response
    }
