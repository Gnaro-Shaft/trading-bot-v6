bot_trading_V6/
│
├── main.py ← boucle principale du bot réel
├── trader.py ← envoi des ordres réels
├── decision_engine.py ← logique de stratégie dynamique
├── binance_api.py ← accès API Binance
├── memory.py ← suivi de la position ouverte
├── notifier.py ← notifications Telegram
├── logger.py ← debug & logs Telegram
├── chart.py ← affichage ASCII des prix
├── config.py ← paramètres globaux
├── trading_log.csv ← historique des PnL
│
├── pnl_logger.py ← enregistrement et affichage PnL
├── show_pnl.py ← script pour afficher manuellement les PnL
│
├── backtester.py ← outil pour comparer les stratégies
├── strategies/
│ ├── **init**.py
│ ├── base_strategy.py
│ ├── conservative.py
│ └── aggressive.py
│
├── .env ← clés API (à exclure du dépôt git)
├── requirements.txt ← dépendances Python
└── README.md ← explication complète du projet

# Bot de Trading BTC/USDC 📈

Bot de trading autonome connecté à Binance Spot. Stratégie évolutive, log Telegram, backtest multi-stratégies, et suivi PnL.

## Fonctions principales

- Achat/Vente automatique en temps réel
- Stratégie dynamique basée sur la volatilité
- Notifications Telegram
- Compte à rebours dans le terminal
- Graphique ASCII en direct
- Journalisation PnL quotidienne (`trading_log.csv`)
- Comparaison de plusieurs stratégies via `backtester.py`

## Utilisation

1. Créer un fichier `.env` :
   BINANCE_API_KEY=... BINANCE_API_SECRET=... TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=...

2. Installer les dépendances :

pip install -r requirements.txt

3. Lancer le bot en réel :

python main.py

4. Afficher le PnL :

python show_pnl.py

5. Comparer les stratégies :

python backtester.py

---

## Stratégies disponibles

- `base` : seuil de vente à 2 %
- `conservative` : seuil à 3 %, achat plus sélectif
- `aggressive` : seuil à 1.5 %, plus de trades

---

## To-do / Améliorations possibles

- Dashboard graphique (Plotly / Dash)
- Base de données MongoDB
- Détection automatique des tendances
- Optimisation via machine learning
