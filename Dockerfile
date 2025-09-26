# Image de base
FROM python:3.13-slim

# Définit le répertoire de travail
WORKDIR /app

# Installe les dépendances
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copie les fichiers locaux dans le conteneur
COPY . .

# Commande exécutée au démarrage du conteneur
EXPOSE 8000
CMD ["fastapi","run","main.py","--host","127.0.0.1","--port","3000"]