from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.dto.ResultatScanDTO import ResultatScanDTO
from app.service.scan import ScanService
from app.database.database import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/scan", tags=["scan"])

@router.post("/")
def predict(file: UploadFile = File(...), session: Session = Depends(get_session)) -> ResultatScanDTO:
    if not file.filename.lower().endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=400, detail="Fichier non supporté")
    
    return ScanService(session).predict(file)