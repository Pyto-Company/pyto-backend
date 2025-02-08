from fastapi import FastAPI, APIRouter
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.utils import get_openapi
from app.api.scan import router as scan_router
from app.api.meteo import router as weather_router
from app.api.plante import router as plant_router
from app.api.utilisateur import router as user_router
from app.api.rappel import router as rappel_router
from app.api.inscription import router as inscription_router
from app.api.dr_pyto import router as drpyto_router
from app.api.health import router as health_router
from app.api.espece import router as espece_router
from app.api.jardin import router as jardin_router

from firebase_admin import credentials, initialize_app

from app.database.database import create_database, create_initial_data, create_tables, drop_database

from starlette.middleware.cors import CORSMiddleware
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.error_middleware import ErrorLoggingMiddleware
from app.middleware.log_middleware import LoggingMiddleware
from app.middleware.https_middleware import HTTPSMiddleware
from dotenv import load_dotenv
import os
import logging

load_dotenv()

ENVIRONNEMENT = os.getenv("ENV")

# Désactiver les logs d'accès d'uvicorn
logging.getLogger("uvicorn.access").disabled = True

router = APIRouter()
router.include_router(router=scan_router)
router.include_router(router=weather_router)
router.include_router(router=plant_router)
router.include_router(router=user_router)
router.include_router(router=rappel_router)
router.include_router(router=inscription_router)
router.include_router(router=drpyto_router)
router.include_router(router=health_router)
router.include_router(router=espece_router)
router.include_router(router=jardin_router)
# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code à exécuter au démarrage
    drop_database()
    create_database()
    create_tables()
    create_initial_data()
    yield
    # Code à exécuter à l'arrêt (cleanup)

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
            "/health",
            "/inscription/token/{user_uid}"
        ]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = []
    
    # Pour toutes les autres routes, on applique la sécurité
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Initialize the app with lifespan
app = FastAPI(
    title="Pyto API", 
    version="1.0.0", 
    lifespan=lifespan,
    servers=[{"url": "https://api.pyto.eu"}] if ENVIRONNEMENT != "development" else None
)
app.include_router(router=router)

# Ajout du middleware d'authentification
# Doit être ajouté après CORS pour assurer le bon fonctionnement des requêtes préflight
app.add_middleware(AuthMiddleware)

if ENVIRONNEMENT != "development":
    app.add_middleware(HTTPSMiddleware)

# Allow CORS for frontend (React) and backend communication
# TODO allow_origins=["http://127.0.0.1:8000"],  # Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(LoggingMiddleware)

# Après le middleware CORS
app.add_middleware(ErrorLoggingMiddleware)

# Remplacer les lignes existantes de configuration OpenAPI par :
if ENVIRONNEMENT == "development":
    app.openapi = custom_openapi

firebase_config = {
  "type": "service_account",
  "project_id": os.getenv("FIREBASE_PROJECT_ID"),
  "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace(r'\n', '\n'),
  "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.getenv("FIREBASE_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40pyto-mobile-app.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_config)
initialize_app(cred)