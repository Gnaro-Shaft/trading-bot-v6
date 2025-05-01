# trader.py

from binance.client import Client
import os
from notifier import send_telegram_message
from binance_api import get_balance
from memory import get_last_trade, clear_trade, save_trade
from pnl_logger import log_trade_pnl
import time
from config import QUANTITY, SYMBOL
from dotenv import load_dotenv
load_dotenv()


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
    try:
        btc_balance = get_balance('BTC')
        if btc_balance < QUANTITY:
            warning = f"⚠️ Vente annulée : solde insuffisant ({btc_balance} BTC dispo, {QUANTITY} requis)"
            print(f"[SELL] {warning}")
            send_telegram_message(warning)
            clear_trade()
            return None

        order = client.order_market_sell(symbol=SYMBOL, quantity=QUANTITY)
        price = float(order['fills'][0]['price'])

        last_trade = get_last_trade()
        entry_price = last_trade['price']
        log_trade_pnl(entry_price, price, QUANTITY)

        clear_trade()
        print(f"[SELL] ✅ Vente de {QUANTITY} BTC à {price} USDC")
        send_telegram_message(f"✅ Vente réelle de {QUANTITY} BTC à {price} USDC")
        return price

    except Exception as e:
        error_msg = f"[ERROR] Vente échouée : {e}"
        print(error_msg)
        send_telegram_message(f"❌ Erreur lors de la vente : {e}")
        return None