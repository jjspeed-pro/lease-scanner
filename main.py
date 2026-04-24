import requests
from bs4 import BeautifulSoup
import os
from telegram import Bot

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=TOKEN)

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def scrape(url, name):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        deals = []

        for a in soup.find_all("a"):
            text = a.text.strip()

            if "€" in text:
                try:
                    price = int(''.join(filter(str.isdigit, text)))
                    if 150 < price < 250:
                        deals.append((name, text, a.get("href")))
                except:
                    pass

        return deals[:3]
    except:
        return []

def main():
    sites = [
        ("ANWB","https://www.anwb.nl/auto/private-lease"),
        ("DirectLease","https://www.directlease.nl/private-lease"),
        ("Justlease","https://www.justlease.nl/private-lease"),
        ("Arval","https://www.arval.nl/private-lease"),
        ("AutoTrack","https://www.autotrack.nl/private-lease"),
        ("Alphabet","https://www.alphabet.com/nl-nl/private-lease"),
        ("Van Mossel","https://www.vanmossel.nl/private-lease"),
        ("Ayvens","https://www.ayvens.com/nl-nl/private-lease"),
        ("XLEasy","https://www.xleasy.nl/private-lease"),
        ("LeaseVergelijker","https://www.leasevergelijker.nl")
    ]

    all_deals = []

    for name, url in sites:
        all_deals += scrape(url, name)

    seen = set()
    unique = []

    for d in all_deals:
        if d[1] not in seen:
            seen.add(d[1])
            unique.append(d)

    for site, text, link in unique[:10]:
        send(f"🔥 {site}\n{text}\n{link}")

if __name__ == "__main__":
    main()
