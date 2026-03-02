# file_poller/nse_client.py

import requests
import time


class NSEClient:
    BASE_URL = "https://www.nseindia.com"
    ANNOUNCEMENT_API = "https://www.nseindia.com/api/corporate-announcements"

    def __init__(self):
        self.session = requests.Session()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com",
            "Connection": "keep-alive",
        }

        self._initialize_session()

    def _initialize_session(self):
        """
        Hit homepage first to establish cookies.
        """
        try:
            self.session.get(self.BASE_URL, headers=self.headers, timeout=10)
        except Exception as e:
            print(f"[NSE INIT ERROR] {e}")

    def fetch_announcements_by_date(self, from_date: str, to_date: str):
        """
        Fetch corporate announcements between dates.
        Date format: DD-MM-YYYY
        """

        params = {
            "from_date": from_date,
            "to_date": to_date
        }

        try:
            response = self.session.get(
                self.ANNOUNCEMENT_API,
                headers=self.headers,
                params=params,
                timeout=20
            )

            if response.status_code != 200:
                print(f"[NSE STATUS ERROR] {response.status_code}")
                return []

            if "application/json" not in response.headers.get("Content-Type", ""):
                print("[NSE BLOCKED] Non-JSON response received")
                return []

            data = response.json()
            time.sleep(2)  # gentle delay

            return data if isinstance(data, list) else data.get("data", [])

        except Exception as e:
            print(f"[NSE FETCH ERROR] {e}")
            return []