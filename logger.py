# logger.py

from config import DEBUG
from notifier import send_telegram_message

def log(message):
    if DEBUG:
        print(f"[DEBUG] {message}")

def log_to_telegram(message):
    """
    Envoie un message de debug sur Telegram si DEBUG = True
    """
    if DEBUG:
        print(f"[DEBUG-TG] {message}")
        send_telegram_message(f"[DEBUG] {message}")
