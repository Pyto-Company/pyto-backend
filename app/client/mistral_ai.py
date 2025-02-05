import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from app.logger.logger import logger

# Charger les variables d'environnement
load_dotenv()

MISTRAL_API_URL="https://api.mistral.ai/v1/agents/completions"

class MistralClient():

    def call_mistral(prompt: str):
        # Préparez les données à envoyer à l'API
        payload = {
            "agent_id": "ag:4d4ca87c:20241207:premiere-version-dr-pyto:047a3ddb",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('MISTRAL_AI_API_KEY')}",
            "Content-Type": "application/json"
        }

        # Faites l'appel API
        try:
            response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            raise HTTPException(
                status_code=503,
                detail="Impossible de se connecter au service Mistral AI"
            )
        except Timeout:
            raise HTTPException(
                status_code=504,
                detail="Le délai d'attente de la réponse Mistral AI a été dépassé"
            )
        except HTTPError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erreur Mistral AI: {e.response.text}"
            )
        except RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur inattendue lors de l'appel à Mistral AI: {str(e)}"
            )
