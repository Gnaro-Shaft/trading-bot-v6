# decision_engine.py
from binance_api import get_current_price, estimate_volatility, get_moving_average
from memory import get_open_trades
from logger import log, log_to_telegram

def get_dynamic_gain_threshold():
    volatility = estimate_volatility()
    return 0.01 + min(volatility * 2, 0.03)  # entre 1% et 4%

def should_buy():
    try:
        price = get_current_price()
        ma = get_moving_average(period=20)  # ou utilise MA_PERIOD depuis config si dispo

        if price is None or ma is None:
            log("❌ Impossible de récupérer le prix ou la moyenne mobile")
            return False

        if not isinstance(price, (int, float)) or not isinstance(ma, (int, float)):
            log("⚠️ Données invalides : prix ou MA ne sont pas numériques")
            return False

        log(f"📈 Prix actuel : {price}")
        log(f"📉 Moyenne mobile : {ma}")

        if price > ma:
            log("⛔ Prix au-dessus de la MA → pas d'achat")
            return False

        log("✅ Signal d'achat détecté")
        return True

    except Exception as e:
        log(f"[ERREUR] during should_buy : {e}")
        return False

def get_profitable_trade_index():
    current_price = get_current_price()
    trades = get_open_trades()
    gain_min = get_dynamic_gain_threshold()

    for i, trade in enumerate(trades):
        buy_price = float(trade["price"])
        gain = (current_price - buy_price) / buy_price

        log(f"[CHECK] Position {i}: Achat à {buy_price}, Gain latent = {gain*100:.2f}% (seuil = {gain_min*100:.2f}%)")

        if gain >= gain_min:
            log_to_telegram(f"✅ Signal de vente détecté : position {i} avec gain +{gain*100:.2f}%")
            return i

    return None
