# providers/instafinancials.py

import requests
from typing import Dict, Optional

class InstaFinancialsClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://instafinancials.com/api/InstaBasic/v1/json"
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def fetch_company_data(
        self,
        lookup_type: str,
        lookup_value: str,
        scope: str = "All",
        webhook_url: Optional[str] = None
    ) -> Dict:
        headers = {
            "Accept": "application/json",
            "user-key": self.api_key   # ✅ CORRECT HEADER
        }

        if webhook_url:
            headers["Webhook"] = webhook_url

        url = f"{self.base_url}/{lookup_type}/{lookup_value}/{scope}"

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
