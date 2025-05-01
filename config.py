# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement du fichier .env

# --- Binance API ---
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Trading ---
SYMBOL = "BTCUSDC"
QUANTITY = 0.0001              # À adapter selon ton capital
GAIN_MIN = 0.02                # 2% de gain net avant vente
SPREAD_MAX = 0.1               # Pas utilisé pour l’instant
MA_PERIOD = 20                 # Moyenne mobile courte
CYCLE_SECONDS = 30             # Temps d’attente entre chaque décision

DEBUG = True  # Active les logs détaillés

