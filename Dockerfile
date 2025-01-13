# Utiliser une image de base Python
FROM python:3.11-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    curl \
    dnsutils \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY ./app /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]