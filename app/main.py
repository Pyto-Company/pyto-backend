from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, APIRouter
from sqlmodel import SQLModel, Session

from model.espece import Espece
from model.utilisateur import Utilisateur
from model.publication import Publication
from model.plante import Plante
from model.commentaire import Commentaire
from model.photo import Photo
from model.maladie import Maladie
from model.rappel import Rappel
from model.entretien import Entretien
from model.message import Message
from model.abonnement import Abonnement
from model.parametrage import Parametrage
from model.scan import Scan
from model.conseil import Conseil
from model.predisposition import Predisposition
from model.symptome import Symptome
from model.traitement import Traitement

from api.scan import router as scan_router
from api.meteo import router as weather_router
from api.connexion import router as auth_router
from api.plante import router as plant_router
from api.utilisateur import router as user_router
from api.jardin import router as jardin_router
from api.rappel import router as rappel_router
from api.inscription import router as inscription_router
from api.dr_pyto import router as drpyto_router

from database.database import create_database, create_initial_data, create_tables_sync, drop_database, engine

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