from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, APIRouter, Request
from sqlmodel import SQLModel, Session
from fastapi.openapi.utils import get_openapi

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
from model.notification import Notification

from api.scan import router as scan_router
from api.meteo import router as weather_router
from api.connexion import router as auth_router
from api.plante import router as plant_router
from api.utilisateur import router as user_router
from api.jardin import router as jardin_router
from api.rappel import router as rappel_router
from api.inscription import router as inscription_router
from api.dr_pyto import router as drpyto_router
from api.health import router as health_router

from database.database import create_database, create_initial_data, create_tables, drop_database, engine

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from middleware.auth_middleware import AuthMiddleware
from middleware.error_middleware import ErrorLoggingMiddleware

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
router.include_router(router=health_router)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    #drop_database()
    #create_database()
    await create_tables()
    await create_initial_data()
    yield  # L'application démarre ici

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="Pyto API",
        version="1.0.0",
        description="API de l'application Pyto",
        routes=app.routes,
    )
    
    # Ajout du composant de sécurité
    openapi_schema["components"] = {
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Entrez votre token JWT ici"
            }
        }
    }
    
    # Application de la sécurité globalement sauf pour les routes exclues
    for path in openapi_schema["paths"]:
        if path in [
            "/connexion/",
            "/inscription/",
            "/inscription/auth/google",
            "/inscription/auth/google/callback",
            "/utilisateur",
            "/health"
        ]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = []
    
    # Pour toutes les autres routes, on applique la sécurité
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

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

# Ajout du middleware d'authentification
# Doit être ajouté après CORS pour assurer le bon fonctionnement des requêtes préflight
app.add_middleware(AuthMiddleware)

# Après le middleware CORS
app.add_middleware(ErrorLoggingMiddleware)

# Remplacer les lignes existantes de configuration OpenAPI par :
app.openapi = custom_openapi