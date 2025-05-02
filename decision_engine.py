# decision_engine.py
from datetime import datetime, timedelta
from binance_api import (
    get_current_price,
    get_moving_average,
    estimate_volatility,
    get_klines
)
from memory import get_open_trades
from logger import log, log_to_telegram
from scoring import compute_signal_score

def get_dynamic_gain_threshold():
    volatility = estimate_volatility()
    return 0.01 + min(volatility * 2, 0.03)  # entre 1% et 4%

def should_buy():
    try:
        price = get_current_price()
        ma20 = get_moving_average(period=20)
        ma50 = get_moving_average(period=50)

        if None in (price, ma20, ma50):
            log("❌ Données insuffisantes (prix/MA)")
            return False

        if price > ma20:
            log("⛔ Prix > MA20 → tendance non propice")
            return False

        if ma20 >= ma50:
            log("⛔ MA20 ≥ MA50 → pas de tendance baissière claire")
            return False

        log("✅ Conditions de tendance validées (prix < MA20 < MA50)")

        # Étape finale : scoring
        score = compute_signal_score()
        log(f"🎯 Score du signal d'achat : {score}/100")

        if score >= 70:
            log_to_telegram(f"✅ Achat validé (score {score})")
            return True
        else:
            log(f"⛔ Score insuffisant ({score}) → pas d'achat")
            return False

    except Exception as e:
        log(f"[ERREUR] should_buy : {e}")
        return False

def get_profitable_trade_index():
    current_price = get_current_price()
    trades = get_open_trades()
    now = datetime.utcnow()

    for i, trade in enumerate(trades):
        buy_price = float(trade["price"])
        quantity = trade["quantity"]
        timestamp = datetime.fromisoformat(trade["timestamp"])
        holding_time = now - timestamp
        gain = (current_price - buy_price) / buy_price

        log(f"[CHECK] Pos {i}: +{gain*100:.2f}% après {holding_time}")

        # Règle stricte : vendre si gain > 1%
        if gain >= 0.01:
            log_to_telegram(f"✅ Vente (gain +{gain*100:.2f}%) — règle > 1%")
            return i

        # Règle patience : vendre si gain > 0.5% et durée > 1h
        elif gain >= 0.005 and holding_time > timedelta(hours=1):
            log_to_telegram(f"⏳ Vente (gain +{gain*100:.2f}%) après > 1h")
            return i

        # Règle libération de capital : gain > 0.3% après 6h
        elif gain >= 0.003 and holding_time > timedelta(hours=6):
            log_to_telegram(f"📤 Vente par ancienneté > 6h (+{gain*100:.2f}%)")
            return i

    return None
