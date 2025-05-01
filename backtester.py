# backtester.py

from binance_api import get_klines
from strategies import base_strategy, conservative, aggressive

strategies = {
    "base": base_strategy.run,
    "conservative": conservative.run,
    "aggressive": aggressive.run
}

def backtest_all():
    df = get_klines(limit=500)  # 500 dernières bougies (1min ou 1h)
    print("\n📊 Résultats des stratégies :\n")
    print("Nom           | PnL %   | Nb Trades")
    print("--------------|---------|-----------")

    for name, strat in strategies.items():
        result = strat(df.copy())
        print(f"{name:<14}| {result['pnl']:>7.2f} | {result['trades']:>9}")

if __name__ == "__main__":
    backtest_all()
