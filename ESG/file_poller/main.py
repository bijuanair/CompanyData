# file_poller/main.py

from sqlalchemy.orm import Session
from datetime import datetime

from .db import SessionLocal
from .models import RawFiling
from .bse_client import BSEClient
from .downloader import download_pdf
from .filters import get_current_fy
from .logger import setup_logger


logger = setup_logger()

# BSE Scrip Codes
TARGET_SCRIP_CODES = {
    "INFY": "500209",
    "TCS": "532540"
}


def save_filing(db: Session, filing: dict):
    try:
        new_filing = RawFiling(
            symbol=filing["symbol"],
            filing_type=filing["filing_type"],
            filing_date=filing["filing_date"],
            financial_year=filing["financial_year"],
            announcement_subject=filing["announcement_subject"],
            source_url=filing["source_url"],
            exchange="BSE",
            status="pending"
        )

        db.add(new_filing)
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False


def run():
    logger.info("Starting BSE API Poller...")

    db = SessionLocal()
    client = BSEClient()

    # Example date range
    from_date = "20250602"
    to_date = "20250602"

    current_fy = get_current_fy()
    total_inserted = 0

    try:
        for symbol, scrip_code in TARGET_SCRIP_CODES.items():

            logger.info(f"Fetching announcements for {symbol} ({scrip_code})")

            announcements = client.fetch_announcements(
                scrip_code=scrip_code,
                from_date=from_date,
                to_date=to_date
            )

            import json
            print(json.dumps(announcements[0], indent=2))
            break

            logger.info(f"Total fetched for {symbol}: {len(announcements)}")

            for a in announcements:

                headline = a.get("HEADLINE", "") or ""
                attachment = a.get("ATTACHMENTNAME")
                attachment_url = None

                if attachment:
                    attachment_url = (
                        "https://www.bseindia.com/xml-data/corpfiling/AttachHis/"
                        + attachment
                    )

                print(f"{symbol} | {headline}")

                if "Business Responsibility" not in headline and "BRSR" not in headline:
                    continue

                filing_data = {
                    "symbol": scrip_code,
                    "filing_type": "Annual Report",
                    "filing_date": a.get("NEWS_DT"),
                    "financial_year": current_fy,
                    "announcement_subject": headline,
                    "source_url": attachment_url
                }

                inserted = save_filing(db, filing_data)

                if inserted:
                    total_inserted += 1

                    if attachment_url:
                        download_pdf(
                            attachment_name=attachment,
                            symbol=scrip_code,
                            financial_year=current_fy
                        )

        logger.info(f"Total new Annual Reports inserted: {total_inserted}")
        logger.info("Poller completed successfully.")

    except Exception as e:
        logger.error(f"Poller failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run()