# main.py
import time
from decision_engine import should_buy, get_profitable_trade_index
from trader import buy, sell_trade_by_index
from chart import show_price_chart
from config import CYCLE_SECONDS

print("\n🔁 Bot de trading multi-trades lancé")

def main_loop():
    while True:
        try:
            if should_buy():
                buy()
            else:
                index = get_profitable_trade_index()
                if index is not None:
                    sell_trade_by_index(index)
                else:
                    print("❌ Aucune position rentable à vendre")

            show_price_chart()

        except Exception as e:
            print(f"[ERREUR] : {e}")

        countdown(CYCLE_SECONDS)


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"\r⏳ Prochaine décision dans {i} sec", end="")
        time.sleep(1)
    print("\r🔁 Nouvelle décision...           ")

if __name__ == "__main__":
    main_loop()



