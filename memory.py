# memory.py

import json
import os

FILE_PATH = "last_trade.json"

def save_trade(trade_data):
    """Sauvegarde un trade (ex: après achat)"""
    with open(FILE_PATH, "w") as f:
        json.dump(trade_data, f)

def get_last_trade():
    """Récupère le dernier trade (ex: pour savoir si on détient une position)"""
    if not os.path.exists(FILE_PATH):
        return None
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def clear_trade():
    """Supprime la dernière position (ex: après vente)"""
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
