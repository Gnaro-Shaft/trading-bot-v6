# decision_engine.py

from binance_api import (
    get_current_price,
    get_moving_average,
    get_klines,
    estimate_volatility
)
from memory import get_last_trade
from config import MA_PERIOD
from logger import log, log_to_telegram


# === DÉCISION D’ACHAT ===

def should_buy():
    price = get_current_price()
    ma = get_moving_average(period=MA_PERIOD)

    log(f"Prix actuel : {price}")
    log(f"Moyenne mobile ({MA_PERIOD}) : {ma}")

    if not is_price_significantly_low():
        log("⛔ Prix pas assez bas (vs plus bas local)")
        return False

    if not is_price_below_ma(price, ma):
        log("⛔ Prix au-dessus de la moyenne mobile")
        return False

    if has_open_position():
        log("⛔ Position déjà ouverte")
        return False

    log_to_telegram("✅ Signal d’achat détecté")
    return True


# === DÉCISION DE VENTE ===

def should_sell():
    last_trade = get_last_trade()

    if not last_trade:
        log("❌ Aucun trade actif trouvé")
        return False

    if not last_trade.get("is_buy"):
        log("⚠️ Le dernier trade n'est pas un achat")
        return False

    if "price" not in last_trade:
        log("⚠️ Le dernier trade ne contient pas de prix")
        return False

    try:
        entry_price = float(last_trade["price"])
    except (ValueError, TypeError):
        log("⚠️ Prix d'achat invalide dans le fichier")
        return False

    current_price = get_current_price()
    gain = (current_price - entry_price) / entry_price

    log(f"📈 Prix actuel : {current_price}")
    log(f"💰 Prix d’achat : {entry_price}")
    log(f"📊 Gain latent : {gain * 100:.2f}%")

    gain_min = get_dynamic_gain_threshold()
    log(f"🎯 Seuil dynamique requis : {gain_min * 100:.2f}%")

    if gain >= gain_min:
        log_to_telegram(f"✅ Vente validée : gain +{gain * 100:.2f}%")
        return True

    log("⏳ Gain insuffisant pour vendre")
    return False



# === COMPOSANTS DYNAMIQUES ===

def get_dynamic_gain_threshold():
    volatility = estimate_volatility()
    threshold = 0.01 + min(volatility * 2, 0.03)  # entre 1% et 4%
    log(f"🎯 Seuil de gain dynamique basé sur volatilité : {threshold*100:.2f}%")
    return threshold


def is_price_significantly_low():
    df = get_klines(limit=MA_PERIOD)
    current = df['close'].iloc[-1]
    recent_min = df['close'].min()
    ratio = (current - recent_min) / recent_min
    log(f"📉 Écart au plus bas local : {ratio*100:.2f}%")
    return ratio < 0.005  # seuil configurable


# === FONCTIONS SIMPLES ===

def is_price_below_ma(price, ma):
    return price < ma

def has_open_position():
    last_trade = get_last_trade()
    return last_trade is not None and last_trade.get('is_buy', False)
