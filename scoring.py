# scoring.py
from binance_api import get_current_price, get_moving_average, get_klines

def compute_signal_score():
    score = 0
    max_score = 100

    price = get_current_price()
    ma20 = get_moving_average(20)
    ma50 = get_moving_average(50)

    if None in (price, ma20, ma50):
        return 0

    # Prix sous MA20 : +25 pts
    if price < ma20:
        score += 25

    # MA20 < MA50 : +25 pts
    if ma20 < ma50:
        score += 25

    # Confirmation par volume ou pinbar : +25 pts
    klines = get_klines(limit=3)
    vol0 = float(klines[-1][5])
    vol1 = float(klines[-2][5])

    open_ = float(klines[-1][1])
    close = float(klines[-1][4])
    low = float(klines[-1][3])
    high = float(klines[-1][2])

    is_pinbar = (high - low > 3 * abs(close - open_)) and (close > open_)
    is_volume_dropping = vol0 < vol1

    if is_pinbar or is_volume_dropping:
        score += 25

    # Gain potentiel (distance MA50 - prix) : +25 pts max si > 2%
    delta = (ma50 - price) / price
    score += min(delta * 100, 25)

    return round(score)
