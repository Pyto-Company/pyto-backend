from http.client import HTTPException
from dotenv import load_dotenv
from firebase_admin import auth
import os
import requests
# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

class FirebaseClient():

    def get_id_token_from_custom_token(self, custom_token: str) -> str:
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={API_KEY}"
        
        # Décoder le custom_token s'il est en bytes
        if isinstance(custom_token, bytes):
            custom_token = custom_token.decode('utf-8')
            
        payload = {
            "token": custom_token,
            "returnSecureToken": True
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["idToken"]


    def get_token(self, uid):
        custom_token = auth.create_custom_token(uid)
        token = self.get_id_token_from_custom_token(custom_token)
        return {"token": token}

    def get_user_info(self, uid):
        try:
            # Retrieve user details by UID
            user = auth.get_user(uid)
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
                "email_verified": user.email_verified,
                "phone_number": user.phone_number,
                "custom_claims": user.custom_claims,
            }
        except auth.UserNotFoundError:
            raise Exception(f"User with UID {uid} not found.")
        except Exception as e:
            raise Exception(f"Error fetching user data: {e}")