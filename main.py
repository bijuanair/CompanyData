# main.py

from providers.instafinancials import InstaFinancialsClient

INSTA_API_KEY = "GfFThPBbnnOS8mCekz7PPxz0lDF9S7FLMtqt9AuIFagrJCubazDdpQ=="

CIN = "L23201MH1959GOI011388"
WEBHOOK_URL = "https://unobvious-flannelly-latesha.ngrok-free.dev/webhook/insta"

client = InstaFinancialsClient(api_key=INSTA_API_KEY)

ack = client.fetch_company_data(
    lookup_type="CompanyCIN",
    lookup_value=CIN,
    scope="All",
    webhook_url=WEBHOOK_URL
)

print("Order accepted:", ack)
