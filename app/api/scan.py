from fastapi import APIRouter, HTTPException, UploadFile, File
from app.dto.resultat_scan import ResultatScanDTO
from app.service.scan import ScanService

router = APIRouter(prefix="/scan", tags=["scan"])

@router.post("/predict")
async def predict(file: UploadFile = File(...)) -> ResultatScanDTO:
    if not file.filename.endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=400, detail="Fichier non supporté")
    
    resultat_scan = await ScanService.predict(file)
    return {"resultat_scan": resultat_scan}
