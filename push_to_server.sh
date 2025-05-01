#!/bin/bash

# Aller dans le dossier du projet
cd "$(dirname "$0")"

python3 version_manager.py bump

# Ajouter tous les fichiers modifiés
git add .

# Demander un message de commit
echo "📝 Message de commit :"
read commit_msg

# Commit + push vers GitHub
git commit -m "$commit_msg"
git push origin main

