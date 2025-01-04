from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set token expiration time

# Configuration de la sécurité OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ConnexionService():

    def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def refresh_access_token(self, refresh_token: str):
        try:
            # Decode and verify the refresh token
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            # Create a new access token
            new_access_token = self.create_access_token(data={"sub": payload["sub"]})
            return {"access_token": new_access_token, "token_type": "bearer"}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
