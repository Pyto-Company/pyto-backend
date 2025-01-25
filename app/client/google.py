from fastapi import Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration OAuth avec Authlib
oauth = OAuth()
google = oauth.register(
    name="google",
    client_id=os.getenv('GOOGLE_CLIENT_ID'),  # ID client de Google
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),  # Secret client de Google
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

class GoogleClient():

    # Route pour démarrer le processus d'inscription avec Google
    def login_via_google(request: Request):
        redirect_uri = "http://127.0.0.1:8000/inscription/auth/google/callback"  # URI de redirection
        return google.authorize_redirect(request, redirect_uri)

    # Callback après authentification avec Google
    def google_callback(request: Request):
        try:
            try:
                # Récupérer le token d'accès
                token = google.authorize_access_token(request)
                print(token)  # Log the token response for debugging
            except Exception as e:
                print(e)
                raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

            user_info = google.get("https://openidconnect.googleapis.com/v1/userinfo", token=token)
            user_data = user_info.json()

            # Exemple de récupération des informations utilisateur
            email = user_data["email"]
            name = user_data["name"]

            # Inscription ou connexion logique (à implémenter selon votre base de données)
            # Exemple simplifié :
            if email:  # Si l'utilisateur est validé
                return {"message": "Connexion réussie", "email": email, "name": name}
            else:
                raise HTTPException(status_code=400, detail="Impossible de valider l'utilisateur Google.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur d'authentification : {str(e)}")
