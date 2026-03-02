# file_poller/bse_client.py

import requests


class BSEClient:
    BASE_URL = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": "https://www.bseindia.com/",
            "Origin": "https://www.bseindia.com"
        }

    def fetch_announcements(self, scrip_code: str, from_date: str, to_date: str):
        """
        Fetch announcements for a given scrip code and date range.

        from_date, to_date format: YYYYMMDD
        Example: 20250702
        """

        all_results = []
        page = 1

        while True:
            params = {
                "pageno": page,
                "strCat": -1,
                "strPrevDate": from_date,
                "strScrip": scrip_code,
                "strSearch": "P",
                "strToDate": to_date,
                "strType": "C",
                "subcategory": -1
            }

            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=self.headers,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            records = data.get("Table", [])

            if not records:
                break

            all_results.extend(records)
            page += 1

        return all_results