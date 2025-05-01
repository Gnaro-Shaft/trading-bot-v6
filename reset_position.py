from memory import clear_trade
from notifier import send_telegram_message

clear_trade()
print("🔁 Position locale réinitialisée.")
send_telegram_message("🧹 Position locale réinitialisée manuellement.")
