# chart.py

import plotext as plt
from binance_api import get_klines

def show_price_chart():
    """
    Affiche un graphique terminal des 30 dernières minutes de prix BTC/USDC.
    """
    try:
        df = get_klines(limit=30)
        closes = df['close'].tolist()
        times = df['timestamp'].tolist()

        plt.clear_figure()
        plt.title("📈 BTC/USDC - 30 dernières minutes")
        plt.xlabel("Bougies (1min)")
        plt.ylabel("Prix (USDC)")
        plt.plot(closes, label="Prix de clôture")
        plt.plotsize(100, 20)
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"[GRAPH] Erreur : {e}")
