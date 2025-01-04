from fastapi import APIRouter, Request

from app.client.google import GoogleClient

router = APIRouter(prefix="/inscription", tags=["inscription"])

# Route pour démarrer le processus d'inscription avec Google
@router.get("/auth/google")
async def login_via_google(request: Request):
    return await GoogleClient.login_via_google(request)


# Callback après authentification avec Google
@router.get("/auth/google/callback")
async def google_callback(request: Request):
    return await GoogleClient.google_callback(request)