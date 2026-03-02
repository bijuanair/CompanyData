""" from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import os

# Setup headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0')
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.bseindia.com/stock-share-price/infosys-ltd/infy/500209/")
    time.sleep(5)  # Wait for JS
    
    # Find announcement links with BRSR keywords
    links = driver.find_elements(By.XPATH, "//a[contains(@href,'.pdf') or contains(text(),'BRSR') or contains(text(),'Business Responsibility')]")
    
    for i, link in enumerate(links[:3]):
        pdf_url = link.get_attribute('href')
        if pdf_url and '{{' not in pdf_url:  # Skip templates
            print(f"Downloading {pdf_url}")
            resp = requests.get(pdf_url, stream=True)
            filename = f"infosys_brsr_{i+1}.pdf"
            with open(filename, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            print(f"Saved {filename}")

finally:
    driver.quit()
 """

import requests

url = "https://nsearchives.nseindia.com/corporate/BSE_20062024151526_BRSR2324.pdf"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers, stream=True)
resp.raise_for_status()

with open("INFOSYS_BRSR_2023_24.pdf", "wb") as f:
    for chunk in resp.iter_content(8192):
        f.write(chunk)

print("Downloaded INFOSYS_BRSR_2023_24.pdf")
