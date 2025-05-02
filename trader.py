# trader.py
from binance.client import Client
from binance_api import client, get_balance, get_current_price
from memory import add_trade, get_open_trades, remove_trade
from pnl_logger import log_trade_pnl
from notifier import send_telegram_message
from config import SYMBOL, QUANTITY

def buy():
    try:
        usdc_balance = get_balance("USDC")
        current_price = get_current_price()
        cost = QUANTITY * current_price

        if usdc_balance < cost:
            print(f"[BUY] ❌ Solde insuffisant : {usdc_balance} USDC (nécessaire : {cost:.2f})")
            send_telegram_message(f"⚠️ Achat annulé : solde USDC insuffisant ({usdc_balance} dispo)")
            return None

        order = client.order_market_buy(symbol=SYMBOL, quantity=QUANTITY)
        price = float(order['fills'][0]['price'])
        add_trade(price, QUANTITY)
        print(f"[BUY] ✅ Achat de {QUANTITY} BTC à {price} USDC")
        send_telegram_message(f"✅ Achat réel de {QUANTITY} BTC à {price} USDC")
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
