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

Dupliquer le fichier .env-template et le renommer en .env

Puis demander les informations à renseigner à Lucas 

### 4) Lancement de l'application

Exécuter la commande suivante :
```
PS C:\Users\uzanl\Documents\GitHub\pyto-backend> uvicorn app.main:app --reload
```

### 5) Swagger

Une fois l'application lancée, ouvrez le lien suivant dans un navigateur : http://127.0.0.1:8000/docs

Pour lancer en debug : https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger 

### 6) Lancement des tests

Exécuter la commande suivante :
```
PS C:\Users\uzanl\Documents\GitHub\pyto-backend> python -m pytest
```