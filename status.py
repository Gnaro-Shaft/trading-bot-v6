# status.py
from memory import get_open_trades
from binance_api import get_current_price
from notifier import send_telegram_message

trades = get_open_trades()
current_price = get_current_price()

message = "\n📊 Positions ouvertes :\n"
if not trades:
    message += "Aucune position enregistrée."
else:
    for i, trade in enumerate(trades):
        buy_price = float(trade['price'])
        quantity = trade['quantity']
        date = trade['timestamp']
        gain = (current_price - buy_price) / buy_price * 100

        message += f"[{i}] {quantity} BTC acheté à {buy_price} USDC le {date[:19]} → Gain latent : {gain:.2f}%\n"

message += f"\n📈 Prix actuel : {current_price} USDC"

print(message)
send_telegram_message(message)
