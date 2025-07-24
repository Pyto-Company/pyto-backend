# Pyto Backend

## Présentation du projet

Pyto est une plateforme innovante dédiée à l'accompagnement des jardiniers, amateurs comme confirmés, dans la gestion de leurs plantes et de leur jardin. Ce backend, développé en Python avec FastAPI, propose des fonctionnalités avancées telles que l'identification de plantes et de maladies via l'IA, la gestion de rappels d'entretien, la centralisation des conseils horticoles, et l'intégration de données météorologiques en temps réel.

## Objectifs
- Offrir un assistant intelligent pour le suivi et l'entretien des plantes.
- Faciliter l'identification des espèces et des maladies grâce à la vision par ordinateur.
- Automatiser les rappels d'entretien personnalisés.
- Centraliser les informations et conseils pour chaque plante.
- Fournir une API sécurisée et performante pour une application mobile ou web.

## Fonctionnalités principales
- **Gestion des utilisateurs** (authentification Firebase, profils, abonnements)
- **Scan d'espèces et de maladies** (modèles EfficientNet, IA)
- **Gestion du jardin** (plantations, entretiens, rappels)
- **Notifications et rappels automatisés**
- **Intégration météo** (OpenWeather, prévisions personnalisées)
- **API RESTful documentée (Swagger)**
- **Sécurité** (middleware, rate limiting, headers, etc.)

## Technologies utilisées
- **Python 3.12** / **FastAPI**
- **PostgreSQL** (via SQLModel/SQLAlchemy)
- **Docker** / **Docker Compose**
- **Firebase** (authentification, notifications)
- **PyTorch** (modèles IA)
- **OpenWeather API**
- **CI/CD prêt pour déploiement cloud**

---

## Installation des outils

Python 3.12.6 : https://www.python.org/downloads/

PostgreSQL 16.6 : https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

## Installation des librairies

Ouvrir un terminal à la racine du projet

Exécuter la commande suivante pour télécharger toutes les librairies nécessaires :
```
pip install -r requirements.txt
```

## Fichier .env

Dupliquer le fichier .env-template et le renommer en .env

Puis demander les informations à renseigner à Lucas

## Lancement de l'application

Exécuter la commande suivante :
```
uvicorn app.main:app --reload
```

## Documentation Swagger

Une fois l'application lancée, ouvrez le lien suivant dans un navigateur : http://127.0.0.1:8000/docs

Pour lancer en debug : https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger

## Lancement des tests

Exécuter la commande suivante :
```
python -m pytest
```

---