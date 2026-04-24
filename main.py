import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os
import re

TOKEN = os.environ["TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

bot = Bot(token=TOKEN)

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

# 🔎 prijzen zoeken (betere methode)
def extract_prices(text):
    deals = []

    matches = re.findall(r'€\s?\d{2,3}', text)

    for m in matches:
        try:
            price = int(re.sub(r'\D', '', m))
            if price <= 300:  # tijdelijk wat hoger voor testen
                deals.append(m)
        except:
            pass

    # dubbele eruit halen
    return list(set(deals))[:5]


def check_site(url, name):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # betere text extractie
        text = soup.get_text(" ", strip=True)

        deals = extract_prices(text)

        if deals:
            msg = f"🔥 {name}\n" + "\n".join(deals)
            send(msg)

    except Exception as e:
        print(f"Error bij {name}: {e}")


# ✅ sites (stabiel)
sites = [
    ("https://www.anwb.nl/auto/private-lease", "ANWB"),
    ("https://www.directlease.nl/private-lease", "DirectLease"),
    ("https://www.justlease.nl/private-lease", "Justlease"),
    ("https://www.autotrack.nl/private-lease", "AutoTrack"),
    ("https://www.vanmossel.nl/private-lease", "Van Mossel"),
    ("https://www.zeeuwenzeeuw.nl/private-lease", "Zeeuw & Zeeuw"),
]

# 🔁 check alles
for url, name in sites:
    check_site(url, name)

# 🔔 JS sites reminder
send("🔎 Extra check:")
send("Ayvens: https://www.ayvens.com/nl-nl/private-lease/")
send("LeasePlan: https://www.leaseplan.com/nl-nl/private-lease/")
