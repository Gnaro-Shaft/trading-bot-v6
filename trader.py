# trader.py
from binance.client import Client
from binance_api import client, get_balance, get_current_price
from memory import add_trade, get_open_trades, remove_trade
from pnl_logger import log_trade_pnl
from notifier import send_telegram_message
from config import SYMBOL, QUANTITY, BUY_PERCENTAGE

def buy():
    try:
        usdc_balance = get_balance("USDC")
        current_price = get_current_price()

        budget = usdc_balance * BUY_PERCENTAGE
        quantity = round(budget / current_price, 6)

        if quantity <= 0:
            print(f"[BUY] ❌ Quantité calculée invalide : {quantity}")
            return None

        order = client.order_market_buy(symbol=SYMBOL, quantity=quantity)
        price = float(order['fills'][0]['price'])
        add_trade(price, quantity)

        print(f"[BUY] ✅ Achat dynamique de {quantity} BTC à {price} USDC")
        send_telegram_message(f"✅ Achat de {quantity:.6f} BTC à {price} USDC (budget {budget:.2f})")
        return price

    except Exception as e:
        print(f"[ERROR] ❌ Achat échoué : {e}")
        send_telegram_message(f"❌ Erreur lors de l'achat : {e}")
        return None

def sell_trade_by_index(index):
    trades = get_open_trades()
    if index >= len(trades):
        print(f"[SELL] ❌ Index {index} invalide")
        return

    trade = trades[index]
    quantity = trade["quantity"]
    entry_price = trade["price"]

    btc_balance = get_balance("BTC")
    if btc_balance < quantity:
        print(f"[SELL] ❌ Solde insuffisant pour vendre {quantity} BTC")
        send_telegram_message("⚠️ Vente annulée : solde insuffisant")
        remove_trade(index)
        return

    try:
        order = client.order_market_sell(symbol=SYMBOL, quantity=quantity)
        price = float(order['fills'][0]['price'])

        log_trade_pnl(entry_price, price, quantity)
        remove_trade(index)

        print(f"[SELL] ✅ Vente de {quantity} BTC à {price} USDC")
        send_telegram_message(f"✅ Vente réelle : {quantity} BTC à {price} USDC")

    except Exception as e:
        print(f"[ERROR] ❌ Vente échouée : {e}")
        send_telegram_message(f"❌ Erreur lors de la vente : {e}")
