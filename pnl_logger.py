# pnl_logger.py

import csv
import os
from datetime import datetime
from collections import defaultdict

FILE_PATH = "trading_log.csv"

def log_trade_pnl(buy_price, sell_price, quantity):
    """
    Enregistre un trade réalisé avec le PnL dans un fichier CSV
    """
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    gain_usdc = (sell_price - buy_price) * quantity
    gain_pct = (sell_price - buy_price) / buy_price * 100

    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Heure", "Prix Achat", "Prix Vente", "Gain %", "Gain USDC"])
        writer.writerow([date, time, buy_price, sell_price, round(gain_pct, 4), round(gain_usdc, 4)])

    print(f"📊 Trade logué : +{gain_pct:.2f}% / +{gain_usdc:.2f} USDC")

def show_daily_pnl():
    """
    Affiche dans le terminal un résumé du PnL par jour (total % et USDC)
    """
    if not os.path.exists(FILE_PATH):
        print("📭 Aucun trade enregistré pour le moment.")
        return

    daily_results = defaultdict(lambda: {"gain_pct": 0, "gain_usdc": 0})

    with open(FILE_PATH, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["Date"]
            daily_results[date]["gain_pct"] += float(row["Gain %"])
            daily_results[date]["gain_usdc"] += float(row["Gain USDC"])

    print("\n📅 Résumé PnL par jour :")
    print("┌────────────┬────────────┬────────────┐")
    print("│    Date    │ Gain %     │ Gain USDC  │")
    print("├────────────┼────────────┼────────────┤")
    for date, data in sorted(daily_results.items()):
        print(f"│ {date} │ {data['gain_pct']:>10.2f}% │ {data['gain_usdc']:>10.2f} │")
    print("└────────────┴────────────┴────────────┘")

_last_pnl_displayed_date = None

def auto_show_daily_pnl():
    """
    Affiche automatiquement le résumé PnL si on change de date (une fois par jour)
    """
    global _last_pnl_displayed_date
    today = datetime.now().strftime("%Y-%m-%d")
    if _last_pnl_displayed_date != today and datetime.now().hour == 23 and datetime.now().minute >= 59:
        show_daily_pnl()
        _last_pnl_displayed_date = today

