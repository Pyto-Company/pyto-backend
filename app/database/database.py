from datetime import datetime
import psycopg2
from sqlmodel import Session
from fastapi import Depends
from typing import Generator
from sqlmodel import Session, SQLModel
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.model.espece import Espece
from app.model.parametrage import Parametrage
from app.model.plante import Plante
from app.model.utilisateur import Utilisateur
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")

POSTGRESQL_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    POSTGRESQL_URL,
    echo=True,
    future=True
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
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
            print(f"Base de données {DB_NAME} supprimée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la base de données : {e}")


def create_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres", host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
        ) 
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cur:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Base de données {DB_NAME} créée.")
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {e}")


async def create_tables_sync():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Erreur lors de la création des tables de la base de données : {e}")


async def create_initial_data():
    try:
        # Get the directory of this script
        current_dir = os.path.dirname(__file__)
        utilisateurs_json_file_path = os.path.join(current_dir, "utilisateurs.json")
        parametrage_json_file_path = os.path.join(current_dir, "parametrage.json")
        especes_json_file_path = os.path.join(current_dir, "especes.json")
        plantes_json_file_path = os.path.join(current_dir, "plantes.json")

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

        async with async_session() as session:
            session.add_all(objects)
            await session.flush()
            await session.commit()
            print("Tables alimentées avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'alimentation des tables de la base de données : {e}")