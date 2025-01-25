from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.client.mistral_ai import MistralClient

router = APIRouter(prefix="/drpyto", tags=["drpyto"])

class MistralRequest(BaseModel):
    prompt: str

@router.post("/call-mistral")
def call_mistral(request: MistralRequest):
    return MistralClient.call_mistral(request.prompt)
