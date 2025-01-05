from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, APIRouter
from sqlmodel import SQLModel, Session

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

from app.api.scan import router as scan_router
from app.api.meteo import router as weather_router
from app.api.connexion import router as auth_router
from app.api.plante import router as plant_router
from app.api.utilisateur import router as user_router
from app.api.jardin import router as jardin_router
from app.api.rappel import router as rappel_router
from app.api.inscription import router as inscription_router
from app.api.dr_pyto import router as drpyto_router

from app.database.database import create_database, create_initial_data, create_tables_sync, drop_database, engine

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

router = APIRouter()
router.include_router(router=scan_router)
router.include_router(router=weather_router)
router.include_router(router=auth_router)
router.include_router(router=plant_router)
router.include_router(router=user_router)
router.include_router(router=jardin_router)
router.include_router(router=rappel_router)
router.include_router(router=inscription_router)
router.include_router(router=drpyto_router)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    drop_database()
    create_database()
    await create_tables_sync()
    await create_initial_data()
    yield  # L'application démarre ici

# Initialize the app with lifespan
app = FastAPI(title="Pyto API", version="1.0.0", lifespan=lifespan)
app.include_router(router=router)

app.add_middleware(SessionMiddleware, secret_key="your_secret_key_here")

# Allow CORS for frontend (React) and backend communication
# TODO allow_origins=["http://127.0.0.1:8000"],  # Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)