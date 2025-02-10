from datetime import datetime
from typing import Dict, List
from fastapi import UploadFile, File

from app.dto.ResultatScanDTO import ResultatScanDTO
from app.model.espece import Espece
from app.model.maladie import Maladie
from app.model.scan import Scan
from app.repository.entretien import EntretienRepository
from app.repository.espece import EspeceRepository
from app.repository.maladie import MaladieRepository
from app.repository.scan import ScanRepository
from app.service.scan_espece import ScanEspeceService
from app.service.scan_maladie import ScanMaladieService
from app.storage.image import ImageStorage
from app.logger.logger import logger
from sqlalchemy.orm import Session

from app.repository.environnement import EnvironnementRepository
from app.repository.traitement import TraitementRepository
from app.repository.predisposition import PredispositionRepository
from app.repository.symptome import SymptomeRepository

class ScanService():

    def __init__(self, session: Session):

        self.session = session

    def predict(self, file: UploadFile = File(...)) -> ResultatScanDTO:
        # Prédiction de l'espèce
        classe_espece_predicted = ScanEspeceService().predict(file)

        # Récupèration de l'espèce par la classe ia
        espece: Espece = EspeceRepository(self.session).get_by_class_ia(classe_espece_predicted)

        # Récupération des maladies de l'espèce
        maladies: List[Maladie] = MaladieRepository(self.session).get_maladies_by_espece_id(espece.id)

        # Prédiction des maladies
        classes_maladies_predicted = ScanMaladieService().predict_all(file)

        # Filtrage des maladies
        maladie: Maladie = self.filtre_maladies(maladies, classes_maladies_predicted)

        # Récupération des conseils d'entretien
        entretiens = EntretienRepository(self.session).get_entretiens_by_espece_id(espece.id)
        environnements = EnvironnementRepository(self.session).get_environnements_by_espece_id(espece.id)

        # Récupération des traitements
        traitements = TraitementRepository(self.session).get_traitements_by_maladie_id(maladie.id)
        predispositions = PredispositionRepository(self.session).get_predispositions_by_maladie_id(maladie.id)
        symptomes = SymptomeRepository(self.session).get_symptomes_by_maladie_id(maladie.id)

        # Stockage de l'image sur le serveur
        filename: str = ImageStorage.save_scan(file)

        resultat_scan = ResultatScanDTO(
            espece=espece,
            maladie=maladie,
            entretiens=entretiens,
            environnements=environnements,
            traitements=traitements,
            predispositions=predispositions,
            symptomes=symptomes
        )


        # Stockage des informations en base
        if resultat_scan.maladie is not None:
            scan = Scan(
                nom_fichier = filename,
                date_creation = datetime.now(),
                maladie_id = resultat_scan.maladie.id,
                espece_id = resultat_scan.espece.id
            )
            ScanRepository(self.session).create(scan)
        else:
            scan = Scan(
                nom_fichier = filename,
                date_creation = datetime.now(),
                espece_id = resultat_scan.espece.id
            )
            ScanRepository(self.session).create(scan)

        return resultat_scan
    

    def filtre_maladies(self, maladies: List[Maladie], classes_maladies_predicted: List[Dict[str, float]]) -> Maladie:
        # Création d'un tableau de classes_ia des maladies
        classes_ia_maladies = [maladie.classe_ia for maladie in maladies]

        filtered_predictions = [
            prediction for prediction in classes_maladies_predicted 
            if prediction["disease"] in classes_ia_maladies
        ]

        # Gestion des maladies filtrées 
        length = len(filtered_predictions)

        if length == 0:
            raise ValueError(f"Aucune maladie détectée pour {classes_maladies_predicted}")

        elif length == 1:
            highest_prediction = max(filtered_predictions, key=lambda x: x["prediction"])
            maladie = [maladie for maladie in maladies if maladie.classe_ia == highest_prediction["disease"]][0]

        return maladie