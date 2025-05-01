# binance_api.py

from binance.client import Client
import os
import time
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# === Clés API stockées en variables d’environnement ===
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

SYMBOL = "BTCUSDC"
INTERVAL = '1m'  # 1 minute
MA_PERIOD = 20

def get_current_price():
    ticker = client.get_symbol_ticker(symbol=SYMBOL)
    return float(ticker['price'])

def get_klines(limit=100):
    """Récupère les chandeliers (klines)"""
    klines = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

def get_moving_average(period=MA_PERIOD):
    df = get_klines(limit=period + 5)
    ma = df['close'].rolling(window=period).mean().iloc[-1]
    return ma

def get_last_trade():
    """
    Placeholder : à remplacer plus tard par une vraie lecture en base ou en mémoire.
    """
    return None  # À personnaliser plus tard pour suivre les positions

def estimate_volatility(period=20):
    """
    Calcule la volatilité basée sur les variations de prix (écart-type des rendements).
    """
    df = get_klines(limit=period + 1)
    df['returns'] = df['close'].pct_change()
    volatility = df['returns'].std()
    return volatility

