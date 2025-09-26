#!/bin/bash
set -e  # Stop script si une commande échoue

echo "===== Début du déploiement ====="

# Variables (tu peux adapter si besoin)
APP_DIR="$HOME/app-lab2"      # Dossier où ton app sera déployée
REPO_BRANCH="main"
ENV_FILE=".env"

mkdir -p "$APP_DIR"
cd "$APP_DIR"

if [ -d ".git" ]; then
    echo "Pull latest changes..."
    git fetch origin "$REPO_BRANCH"
    git reset --hard "origin/$REPO_BRANCH"
else
    echo "Cloning repo..."
    git clone -b "$REPO_BRANCH" https://github.com/MaxChmt/log430-a25-labo2.git .
fi

# Créer / mettre à jour le fichier .env
echo "Création du fichier .env"
cat > "$ENV_FILE" <<EOL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=labo02_db
DB_USER=labo02
DB_PASS=${DB_PASS}
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
EOL

# Installer / mettre à jour les dépendances Python
echo "Installation des dépendances Python..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations / initialiser la base MySQL
echo "Initialisation de la base de données..."
mysql -h 127.0.0.1 -uroot -p"$DB_ROOT_PASSWORD" labo02_db < db-init/init.sql

echo "===== Déploiement terminé avec succès ====="