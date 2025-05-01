# notifier.py

import os
import requests
from config import TELEGRAM_BOT_TOKEN as BOT_TOKEN, TELEGRAM_CHAT_ID as CHAT_ID


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """
    Envoie un message à ton Telegram via le bot
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("[NOTIF] ⚠️ Telegram non configuré")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[NOTIF] ⚠️ Erreur d'envoi Telegram : {response.text}")
    except Exception as e:
        print(f"[NOTIF] ⚠️ Exception : {e}")
