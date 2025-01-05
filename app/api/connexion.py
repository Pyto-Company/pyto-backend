from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from service.connexion import ConnexionService

router = APIRouter(prefix="/connexion", tags=["connexion"])

class User(BaseModel):
    username: str
    password: str  # In a real app, passwords should be hashed

@router.post("/")
async def login_for_access_token(form_data: User):
    # Here you would normally verify the user's credentials against a database
    if form_data.username != "test" or form_data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create the access token
    connexion_service = ConnexionService()
    access_token = connexion_service.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    return ConnexionService.refresh_access_token(refresh_token)