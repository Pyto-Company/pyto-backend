from datetime import datetime, time
import psycopg2
from sqlmodel import SQLModel
import json
import os
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy import text
import traceback
from app.logger.logger import logger
import logging
from fastapi import Depends
from dotenv import load_dotenv

from app.model.espece import Espece
from app.model.utilisateur import Utilisateur
from app.model.publication import Publication
from app.model.plante import Plante
from app.model.commentaire import Commentaire
from app.model.photo import Photo
from app.model.maladie import Maladie
from app.model.rappel import Rappel
from app.model.entretien import Entretien
from app.model.message import Message
from app.model.abonnement import Abonnement
from app.model.parametrage import Parametrage
from app.model.scan import Scan
from app.model.conseil import Conseil
from app.model.predisposition import Predisposition
from app.model.symptome import Symptome
from app.model.traitement import Traitement
from app.model.notification import Notification
from app.model.plantation import Plantation

# Charger les variables d'environnement
load_dotenv()

# Configurer le logging de SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

DB_HOST = os.getenv('DATABASE_HOST')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_PORT = os.getenv('DATABASE_PORT')
DB_NAME = os.getenv('DATABASE_NAME')

POSTGRESQL_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    POSTGRESQL_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pour l'injection de dépendance
def get_db():
    with SessionLocal() as db:
        yield db

SessionDep = Depends(get_db)

def drop_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres", host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
        ) 
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cur:
            # Terminer les connexions actives
            cur.execute(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{DB_NAME}'
                    AND pid <> pg_backend_pid();
                """
            )
            # Supprimer la base de données
            cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
            logger.info(f"Base de données {DB_NAME} supprimée.")
    except Exception as e:
        logger.error(
            f"Erreur lors de la suppression de la base de données:\n"
            f"Operation: drop_database \n"
            f"Database: {DB_NAME}\n"
            f"Host: {DB_HOST}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )

def create_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres", host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
        ) 
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cur:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            logger.info(f"Base de données {DB_NAME} créée.")
    except Exception as e:
        logger.error(
            f"Erreur lors de la création de la base de données:\n"
            f"Operation: create_database \n"
            f"Database: {DB_NAME}\n"
            f"Host: {DB_HOST}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )

def create_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Tables créées avec succès.")
    except Exception as e:
        logger.error(
            f"Erreur lors de la création des tables:\n"
            f"POSTGRESQL_URL: {POSTGRESQL_URL}\n"
            f"Operation: create_tables \n"
            f"Database: {DB_NAME}\n"
            f"Host: {DB_HOST}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )

def create_initial_data():
    try:
        # Get the directory of this script
        current_dir = os.path.dirname(__file__)
        utilisateurs_json_file_path = os.path.join(current_dir, "utilisateurs.json")
        parametrage_json_file_path = os.path.join(current_dir, "parametrage.json")
        especes_json_file_path = os.path.join(current_dir, "especes.json")
        plantes_json_file_path = os.path.join(current_dir, "plantes.json")
        rappels_json_file_path = os.path.join(current_dir, "rappels.json")
        notifications_json_file_path = os.path.join(current_dir, "notifications.json")
        plantations_json_file_path = os.path.join(current_dir, "plantations.json")
        abonnements_json_file_path = os.path.join(current_dir, "abonnements.json")
        entretiens_json_file_path = os.path.join(current_dir, "entretiens.json")
        maladies_json_file_path = os.path.join(current_dir, "maladies.json")

        with open(utilisateurs_json_file_path, "r", encoding="utf-8") as file:
            objects = [Utilisateur(**elem) for elem in json.load(file)]

        with open(parametrage_json_file_path, "r", encoding="utf-8") as file:
            objects += [Parametrage(**elem) for elem in json.load(file)]

        with open(especes_json_file_path, "r", encoding="utf-8") as file:
            objects += [Espece(**elem) for elem in json.load(file)]

        with open(plantes_json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for plante in data:
                if "date_creation" in plante:
                    plante["date_creation"] = datetime.fromisoformat(plante["date_creation"])
            objects += [Plante(**elem) for elem in data]

        with open(entretiens_json_file_path, "r", encoding="utf-8") as file:
            objects += [Entretien(**elem) for elem in json.load(file)]

        with open(rappels_json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for rappel in data:
                if "date_creation" in rappel:
                    rappel["date_creation"] = datetime.fromisoformat(rappel["date_creation"])
                if "heure" in rappel:
                    rappel["heure"] = time.fromisoformat(rappel['heure'])
            objects += [Rappel(**elem) for elem in data]

        with open(notifications_json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for notification in data:
                if "date_creation" in notification:
                    notification["date_creation"] = datetime.fromisoformat(notification["date_creation"])
            objects += [Notification(**elem) for elem in data]

        with open(plantations_json_file_path, "r", encoding="utf-8") as file:
            objects += [Plantation(**elem) for elem in json.load(file)]

        with open(abonnements_json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for abonnement in data:
                if "date_debut" in abonnement:
                    abonnement["date_debut"] = datetime.fromisoformat(abonnement["date_debut"])
            objects += [Abonnement(**elem) for elem in data]

        with open(maladies_json_file_path, "r", encoding="utf-8") as file:
            objects += [Maladie(**elem) for elem in json.load(file)]

        with SessionLocal() as session:
            session.add_all(objects)
            session.flush()
            
            # Réinitialiser la séquence d'ID pour la table utilisateur
            session.execute(
                text("SELECT setval('utilisateur_id_seq', (SELECT MAX(id) FROM utilisateur))")
            )

            # Réinitialiser la séquence d'ID pour la table rappel
            session.execute(
                text("SELECT setval('rappel_id_seq', (SELECT MAX(id) FROM rappel))")
            )
            
            session.commit()
            logger.info("Tables alimentées avec succès.")

    except Exception as e:
        logger.error(
            f"Erreur lors de l'alimentation des tables de la base de données:\n"
            f"Operation: create_initial_data \n"
            f"Database: {DB_NAME}\n"
            f"Host: {DB_HOST}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
