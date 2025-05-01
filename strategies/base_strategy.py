# strategies/base_strategy.py

def run(df):
    position = None
    entry_price = 0
    pnl = 0
    trades = 0

    for i in range(1, len(df)):
        price = df['close'].iloc[i]
        ma = df['close'].rolling(window=20).mean().iloc[i]

        if position is None and price < ma:
            position = price
            trades += 1

        elif position is not None and price > position * 1.02:
            pnl += (price - position)
            position = None

    return {
        "pnl": pnl,       # brut
        "trades": trades
    }
