# memory.py
import os
import json

FILE_PATH = "last_trade.json"

def save_trade(price, is_buy=True):
    """
    Sauvegarde le dernier trade dans un fichier local.
    """
    trade = {
        "price": price,
        "is_buy": is_buy
    }
    with open(FILE_PATH, "w") as f:
        json.dump(trade, f)

def get_last_trade():
    """
    Lit les infos du dernier trade (si dispo).
    Retourne None si le fichier est vide ou corrompu.
    """
    if not os.path.exists(FILE_PATH):
        return None

    try:
        with open(FILE_PATH, "r") as f:
            trade = json.load(f)
            if "price" in trade and "is_buy" in trade:
                return trade
            else:
                return None
    except (json.JSONDecodeError, IOError):
        return None

def has_open_position():
    """
    Retourne True si un trade d'achat est enregistré.
    """
    last_trade = get_last_trade()
    return last_trade is not None and last_trade.get("is_buy", False)

def clear_trade():
    """
    Supprime la mémoire locale du dernier trade.
    """
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
