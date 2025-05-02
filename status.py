# status.py
from memory import get_open_trades
from binance_api import get_current_price

trades = get_open_trades()
current_price = get_current_price()

print("\n📊 Positions ouvertes :\n")
if not trades:
    print("Aucune position enregistrée.")
else:
    for i, trade in enumerate(trades):
        buy_price = float(trade['price'])
        quantity = trade['quantity']
        date = trade['timestamp']
        gain = (current_price - buy_price) / buy_price * 100

        print(f"[{i}] {quantity} BTC acheté à {buy_price} USDC le {date[:19]} → Gain latent : {gain:.2f}%")

print(f"\n📈 Prix actuel : {current_price} USDC")
