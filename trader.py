# trader.py

from binance.client import Client
import os
from memory import save_trade, clear_trade, get_last_trade
import time
from config import BINANCE_API_KEY, BINANCE_API_SECRET, SYMBOL, QUANTITY
from pnl_logger import log_trade_pnl


API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

SYMBOL = "BTCUSDC"
QUANTITY = 0.0001  # À ajuster selon tes fonds

def buy():
    """
    Passe un ordre d'achat au marché
    """
    try:
        order = client.order_market_buy(symbol=SYMBOL, quantity=QUANTITY)
        price = float(order['fills'][0]['price'])
        save_trade({
            "price": price,
            "time": int(time.time()),
            "is_buy": True
        })
        print(f"[BUY] Achat de {QUANTITY} BTC à {price} USDC")
        return price
    except Exception as e:
        print(f"[ERROR] Achat échoué : {e}")
        return None

def sell():
    """
    Passe un ordre de vente au marché
    """
    try:
        order = client.order_market_sell(symbol=SYMBOL, quantity=QUANTITY)
        price = float(order['fills'][0]['price'])
        last_trade = get_last_trade()
        entry_price = last_trade['price']
        log_trade_pnl(entry_price, price, QUANTITY)
        clear_trade()
        print(f"[SELL] Vente de {QUANTITY} BTC à {price} USDC")
        return price
    except Exception as e:
        print(f"[ERROR] Vente échouée : {e}")
        return None
