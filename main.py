from telegram import Bot
import os

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=TOKEN)

bot.send_message(chat_id=CHAT_ID, text="🔥 TEST: je bot werkt!")
