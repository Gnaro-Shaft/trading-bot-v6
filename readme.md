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

MaJ 02/05/2025

# 🧠 Stratégie de Trading - Résumé Documenté

## 🎯 Objectif

Automatiser les décisions d'achat et de vente de BTC/USDC en appliquant une stratégie évolutive, intelligente, et sécurisée.

---

## ✅ Conditions d'Achat (`should_buy()`)

### 1. **Filtre de Tendance**

- Le prix actuel doit être **inférieur à la MA20** (moyenne mobile 20 périodes)
- Et **MA20 < MA50** (tendance baissière claire)

### 2. **Scoring Global (0–100)** via `scoring.py`

Le score est basé sur 4 critères :

- 📉 Prix < MA20 → +25 pts
- 📉 MA20 < MA50 → +25 pts
- 📊 Volume en baisse ou bougie pinbar → +25 pts
- 📈 Distance de MA50 (gain potentiel) → jusqu’à +25 pts

✅ Achat validé si score ≥ **70**

---

## ✅ Conditions de Vente (`get_profitable_trade_index()`)

### 🔒 Règles de sécurité et de rentabilité :

1. **Vente immédiate** si gain ≥ **1.00 %**
2. **Vente après 1h** si gain ≥ **0.50 %**
3. **Vente après 6h** si gain ≥ **0.30 %**

Chaque position est vérifiée individuellement (multi-trades supporté).

---

## 📦 Structure mémoire (multi-trades)

Stockée dans `open_trades.json` :

```json
[
  { "price": 94500.0, "quantity": 0.0001, "timestamp": "2025-05-01T21:03:44" },
  { "price": 95100.0, "quantity": 0.0001, "timestamp": "2025-05-01T21:22:01" }
]
```

---

## 📲 Notifications Telegram

- ✅ Achat validé (score)
- ✅ Vente (avec % de gain)
- ⚠️ Solde insuffisant
- ❌ Erreurs API

---

## 🔧 Fichiers clés

- `decision_engine.py` → stratégie d'achat/vente
- `scoring.py` → score du signal d'achat
- `memory.py` → mémoire des positions
- `trader.py` → exécution des ordres
- `status.py` → affichage des positions

---

## 🔁 Boucle principale (`main.py`)

1. Vérifie si achat est possible via `should_buy()`
2. Sinon, tente de vendre la meilleure position rentable
3. Rafraîchissement automatique + logs

---

## 🛠️ À venir (si activé)

- Détection de divergence RSI
- Suivi du PnL quotidien via calendrier visuel
- Dashboard interactif Dash / Plotly

---

> Dernière mise à jour : `2025-05-01`
