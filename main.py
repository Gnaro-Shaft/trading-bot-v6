# main.py

import time
from dotenv import load_dotenv
from decision_engine import should_buy, should_sell
from trader import buy, sell
from binance_api import get_current_price
from notifier import send_telegram_message
from config import QUANTITY, SYMBOL, CYCLE_SECONDS
import sys
from chart import show_price_chart
from pnl_logger import show_daily_pnl
from pnl_logger import auto_show_daily_pnl



load_dotenv()  # Charge les clés API depuis le fichier .env

CYCLE_SECONDS = 60  # une décision par minute

def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Prochaine décision dans {i} sec")
        sys.stdout.flush()
        time.sleep(1)
    print("\r🔁 Nouvelle décision...           ")

def main_loop():
    print("🔁 Bot de trading démarré.")
    while True:
        try:
            price = get_current_price()
            print(f"\n📈 Prix actuel : {price} USDC")

            if should_buy():
                print("✅ Décision : Acheter")
                buy()
                send_telegram_message(f"✅ Achat de {QUANTITY} BTC à {price} USDC")

            elif should_sell():
                print("✅ Décision : Vendre")
                sell()
                send_telegram_message(f"✅ Vente de {QUANTITY} BTC à {price} USDC")

            else:
                print("❌ Aucune action à faire pour l’instant")

        except Exception as e:
            print(f"[ERREUR] : {e}")

        auto_show_daily_pnl()
        
        countdown(CYCLE_SECONDS)
        show_price_chart()

if __name__ == "__main__":
    main_loop()
    show_daily_pnl()
    
    


