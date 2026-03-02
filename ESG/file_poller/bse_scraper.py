# file_poller/bse_scraper.py

from playwright.sync_api import sync_playwright


class BSEScraper:

    def fetch_announcements(self, from_date=None, to_date=None):
        """
        Date format: DD/MM/YYYY
        Example: 02/07/2025
        """

        announcements = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://www.bseindia.com/corporates/ann.html")

            # Wait until page is fully loaded
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # If date range provided, fill and submit
            # if from_date and to_date:
            #     try:
            #         page.fill(
            #             "input[name='ctl00$ContentPlaceHolder1$txtFromDate']",
            #             from_date
            #         )

            #         page.fill(
            #             "input[name='ctl00$ContentPlaceHolder1$txtToDate']",
            #             to_date
            #         )

            #         page.click(
            #             "input[name='ctl00$ContentPlaceHolder1$btnSubmit']"
            #         )

            #         # Wait for results table to refresh
            #         page.wait_for_load_state("networkidle")
            #         page.wait_for_timeout(3000)

            #     except Exception as e:
            #         print(f"[DATE FILTER ERROR] {e}")

            if from_date and to_date:
                try:
                    # Focus and replace From Date
                    from_input = page.locator("input[name='ctl00$ContentPlaceHolder1$txtFromDate']")
                    from_input.click()
                    from_input.press("Control+A")
                    from_input.type(from_date)

                    # Focus and replace To Date
                    to_input = page.locator("input[name='ctl00$ContentPlaceHolder1$txtToDate']")
                    to_input.click()
                    to_input.press("Control+A")
                    to_input.type(to_date)

                    # Click Submit
                    page.locator("input[name='ctl00$ContentPlaceHolder1$btnSubmit']").click()

                    # Wait for table to refresh properly
                    page.wait_for_timeout(5000)

                except Exception as e:
                    print(f"[DATE FILTER ERROR] {e}")

            # Ensure table exists
            #page.wait_for_selector("table")
            page.wait_for_selector("table tr")
            
            rows = page.query_selector_all("table tr")

            for row in rows[1:]:  # skip header
                cols = row.query_selector_all("td")

                if len(cols) < 5:
                    continue

                scrip_code = cols[0].inner_text().strip()
                company_name = cols[1].inner_text().strip()
                headline = cols[2].inner_text().strip()
                date = cols[3].inner_text().strip()

                link_element = cols[2].query_selector("a")
                attachment_url = None

                if link_element:
                    attachment_url = link_element.get_attribute("href")

                    if attachment_url and not attachment_url.startswith("http"):
                        attachment_url = "https://www.bseindia.com" + attachment_url

                announcements.append({
                    "scrip_code": scrip_code,
                    "company_name": company_name,
                    "headline": headline,
                    "date": date,
                    "attachment_url": attachment_url
                })

            browser.close()

        return announcements