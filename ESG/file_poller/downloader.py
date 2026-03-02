import requests
import os


def download_pdf(attachment_name, symbol, financial_year):
    """
    Downloads PDF from BSE with proper headers to avoid 403.
    """

    url = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{attachment_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.bseindia.com/",
        "Origin": "https://www.bseindia.com",
        "Accept": "application/pdf"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"[DOWNLOAD FAILED] Status {response.status_code}")
            return

        # Create folder structure
        folder_path = os.path.join("data", symbol, financial_year)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, attachment_name)

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"[DOWNLOADED] {file_path}")

    except Exception as e:
        print(f"[DOWNLOAD ERROR] {e}")