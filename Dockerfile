# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier d'abord les requirements pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances en gardant le cache pip
RUN pip install -r requirements.txt

# Copier le reste des fichiers
COPY ./app /app

# Exposer le port
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]