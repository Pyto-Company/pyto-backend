from datetime import datetime, time
import psycopg2
from sqlmodel import Session
from fastapi import Depends
from typing import AsyncGenerator
from sqlmodel import Session, SQLModel
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import traceback
from model.abonnement import Abonnement
from model.plantation import Plantation
from model.notification import Notification
from model.rappel import Rappel
from logger.logger import logger
import logging

from model.espece import Espece
from model.parametrage import Parametrage
from model.plante import Plante
from model.utilisateur import Utilisateur
from dotenv import load_dotenv

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

POSTGRESQL_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    POSTGRESQL_URL,
    echo=False,  # Désactiver l'echo des requêtes SQL
    future=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDep = Depends(get_session)

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

async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
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

async def create_initial_data():
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

        async with async_session() as session:
            session.add_all(objects)
            await session.flush()
            
            # Réinitialiser la séquence d'ID pour la table utilisateur
            await session.execute(
                text("SELECT setval('utilisateur_id_seq', (SELECT MAX(id) FROM utilisateur))")
            )
            
            await session.commit()
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