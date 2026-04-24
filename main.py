import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

TOKEN = os.environ["TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

bot = Bot(token=TOKEN)

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def extract_prices(text):
    deals = []
    for line in text.split("\n"):
        if "€" in line:
            try:
                price = int(''.join(filter(str.isdigit, line)))
                if 150 < price <= 250:
                    deals.append(line.strip())
            except:
                pass
    return deals[:3]

def check_site(url, name):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        deals = extract_prices(text)

        if deals:
            msg = f"🔥 {name}\n\n" + "\n".join(deals)
            send(msg)

    except Exception as e:
        print(f"Error {name}: {e}")

# ✅ Werkende sites
sites = [
    ("https://www.anwb.nl/auto/private-lease", "ANWB"),
    ("https://www.directlease.nl/private-lease", "DirectLease"),
    ("https://www.justlease.nl/private-lease", "Justlease"),
    ("https://www.autotrack.nl/private-lease", "AutoTrack"),
    ("https://www.vanmossel.nl/private-lease", "Van Mossel"),
    ("https://www.zeeuwenzeeuw.nl/private-lease", "Zeeuw & Zeeuw"),
]

# 🔍 Check werkende sites
for url, name in sites:
    check_site(url, name)

# ⚠️ JS sites (handmatig check melding)
send("🔎 Check ook deze sites (JS):")
send("Ayvens: https://www.ayvens.com/nl-nl/private-lease/")
send("LeasePlan: https://www.leaseplan.com/nl-nl/private-lease/")
