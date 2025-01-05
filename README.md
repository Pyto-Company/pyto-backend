### 1) Installation des outils 

Python 3.12.6 : https://www.python.org/downloads/

PostgreSQL 16.6 : https://www.enterprisedb.com/downloads/postgres-postgresql-downloads 

### 2) Installation des librairies 

Ouvrir un terminal à la racine du projet

Exécuter la commande suivante pour télécharger toutes les librairies nécessaires : 
```
pip install -r requirements.txt
```

### 3) Fichier .env

A la racine du projet, créer un fichier ".env" avec le contenu suivant : 
```
GOOGLE_CLIENT_ID={demander à Lucas}
GOOGLE_CLIENT_SECRET={demander à Lucas}
MISTRAL_AI_API_KEY={demander à Lucas}
OPEN_WEATHER_API_KEY={demander à Lucas}
DATABASE_HOST = "localhost"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "votremotdepasse"
DATABASE_PORT = 5432
DATABASE_NAME = "pyto"
```

### 4) Lancement de l'application

Exécuter la commande suivante :
```
uvicorn main:app --reload
```

### 5) Swagger

Une fois l'application lancée, ouvrez le lien suivant dans un navigateur : http://127.0.0.1:8000/docs

Pour lancer en debug : https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger 