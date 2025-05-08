#!/bin/bash

# 📍 Se placer dans le dossier du projet
cd ~/trading-bot-v6 || {
  echo "❌ Le dossier ~/trading-bot-v6 n'existe pas.";
  exit 1
}

# 🔄 Mettre à jour le projet depuis GitHub
echo "🚀 Mise à jour du dépôt Git..."
git fetch origin && git reset --hard origin/main || {
  echo "❌ Échec de la mise à jour Git";
  exit 1
}

# 🐳 Rebuild de l'image Docker
echo "🔧 Reconstruction de l'image Docker..."
docker build -t trading-bot . || {
  echo "❌ Échec du build Docker";
  exit 1
}

# ⛔ Arrêt et suppression de l'ancien conteneur
echo "🧼 Nettoyage de l'ancien conteneur..."
docker stop my-bot 2>/dev/null
docker rm my-bot 2>/dev/null

# 🚀 Lancement du nouveau conteneur
echo "▶️ Lancement du nouveau conteneur..."
docker run -d --name my-bot \
  --env-file .env \
  --restart unless-stopped \
  trading-bot || {
    echo "❌ Échec du lancement du conteneur";
    exit 1
}

echo "✅ Mise à jour et redémarrage terminés avec succès."
