import asyncpg
from fastapi import APIRouter
import psycopg2
import os
from dotenv import load_dotenv
from logger.logger import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    load_dotenv()
    db_info = {
        "status": "checking",
        "database_host": os.getenv('DATABASE_HOST'),
        "database_port": os.getenv('DATABASE_PORT'),
        "database_name": os.getenv('DATABASE_NAME'),
        "connection_error": None
    }
    
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT')
        )
        db_info["status"] = "healthy"
        connection.close()
    except Exception as e:
        db_info["status"] = "unhealthy"
        db_info["connection_error"] = str(e)
        logger.error(f"Erreur de connexion PostgreSQL: {str(e)}")
    
    return db_info

@router.get("/healthasync")
async def health_check():
    load_dotenv()
    db_info = {
        "status": "checking",
        "database_host": os.getenv('DATABASE_HOST'),
        "database_port": os.getenv('DATABASE_PORT'),
        "database_name": os.getenv('DATABASE_NAME'),
        "connection_error": None
    }
    
    try:
        connection = await asyncpg.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT')
        )
        db_info["status"] = "healthy"
        connection.close()
    except Exception as e:
        db_info["status"] = "unhealthy"
        db_info["connection_error"] = str(e)
        logger.error(f"Erreur de connexion PostgreSQL: {str(e)}")
    
    return db_info