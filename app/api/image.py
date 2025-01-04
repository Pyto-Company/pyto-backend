from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/image", tags=["image"])

BASE_IMAGE_DIR = "path/to/image/directory"

@router.get("/")
def getImage(cheminImage: str):
    
    image_path = (
        os.path.join(BASE_IMAGE_DIR, cheminImage)
        if cheminImage
        else None
    )
    
    if not image_path or not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path, media_type="image/jpeg")