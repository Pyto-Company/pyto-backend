import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
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

pytest_plugins = ('pytest_asyncio',)

@pytest_asyncio.fixture(scope="session")
async def engine():
    POSTGRESQL_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_async_engine(
        POSTGRESQL_URL,
        echo=False,
        future=True,
        pool_pre_ping=True
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def async_session_test(engine):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session

@pytest_asyncio.fixture(scope="session")
async def setup_database(engine):
    from app.database.database import drop_database, create_database, create_tables, create_initial_data
    drop_database()
    create_database()
    await create_tables()
    await create_initial_data()
    yield

@pytest_asyncio.fixture
async def session(async_session_test, setup_database) -> AsyncSession:
    async with async_session_test() as session:
        yield session