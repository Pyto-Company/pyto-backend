import os
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

# Charger les variables d'environnement
load_dotenv()

MISTRAL_API_URL="https://api.mistral.ai/v1/agents/completions"

class MistralClient():

    async def call_mistral(prompt: str):
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
            "Authorization": f"Bearer {os.getenv("MISTRAL_AI_API_KEY")}",
            "Content-Type": "application/json"
        }

        # Faites l'appel API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(MISTRAL_API_URL, json=payload, headers=headers)
                response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erreur depuis Mistral AI: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur interne: {str(e)}"
            )
