# memory.py
import os
import json
from datetime import datetime

FILE_PATH = "open_trades.json"

def _load_trades():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r") as f:
            trades = json.load(f)
            if isinstance(trades, list):
                return trades
            return []
    except (json.JSONDecodeError, IOError):
        return []

def _save_trades(trades):
    with open(FILE_PATH, "w") as f:
        json.dump(trades, f, indent=2)

def add_trade(price, quantity):
    trades = _load_trades()
    trades.append({
        "price": price,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat()
    })
    _save_trades(trades)

def get_open_trades():
    return _load_trades()

def remove_trade(index):
    trades = _load_trades()
    if 0 <= index < len(trades):
        removed = trades.pop(index)
        _save_trades(trades)
        return removed
    return None

def clear_all_trades():
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

def has_open_trades():
    return len(_load_trades()) > 0
