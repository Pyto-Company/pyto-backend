from datetime import datetime
from typing import Dict, List
from fastapi import UploadFile, File

from dto.resultat_scan import ResultatScanDTO
from model.espece import Espece
from model.maladie import Maladie
from model.scan import Scan
from repository.entretien import EntretienRepository
from repository.espece import EspeceRepository
from repository.maladie import MaladieRepository
from repository.scan import ScanRepository
from service.scan_espece import ScanEspeceService
from service.scan_maladie import ScanMaladieService
from storage.image import ImageStorage
from logger.logger import logger

class ScanService():

    async def predict(self, file: UploadFile = File(...)) -> ResultatScanDTO:
        # Préparation du retour
        resultat_scan = ResultatScanDTO()

        # Prédiction de l'espèce
        classe_espece_predicted = ScanEspeceService.predict(file)

        # Récupèration de l'espèce par la classe ia
        espece: Espece = EspeceRepository.get_by_class_ia(classe_espece_predicted)
        resultat_scan.espece = espece

        # Récupération des maladies de l'espèce
        maladies: List[Maladie] = MaladieRepository.get_maladies_by_espece_id(espece.id)

        # Prédiction des maladies
        classes_maladies_predicted = ScanMaladieService.predict_all(file)

        # Filtrage des maladies
        maladies_predicted: List[Maladie] = self.filtre_maladies(maladies, classes_maladies_predicted)

        # Gestion des maladies filtrées 
        length = len(maladies_predicted)
        if length == 0:
            logger.error("Aucune maladie détectée")
        elif length == 1:
            logger.info("Une seule maladie détectée")
            resultat_scan.maladie = maladies_predicted[0]
        else:
            logger.error("Plus d'une maladie détectée")

        # Récupération des conseils d'entretien
        resultat_scan.entretiens = EntretienRepository.get_entretien_by_espece_id(espece.id)

        # Stockage de l'image sur le serveur
        filename: str = ImageStorage.save_scan()

        # Stockage des informations en base
        if resultat_scan.maladie is not None:
            scan = Scan(
                nom_fichier = filename,
                date_creation = datetime.now(),
                maladie_id = resultat_scan.maladie.id,
                espece_id = resultat_scan.espece.id
            )
            ScanRepository.create(scan)
        else:
            scan = Scan(
                nom_fichier = filename,
                date_creation = datetime.now(),
                espece_id = resultat_scan.espece.id
            )
            ScanRepository.create(scan)

        return resultat_scan
    

    def filtre_maladies(self, maladies: List[Maladie], classes_maladies_predicted: List[Dict[str, float]]) -> List[Maladie]:
        # Création d'un tableau de classes_ia des maladies
        classes_ia_maladies = [maladie.classe_ia for maladie in maladies]

        filtered_predictions = [
            prediction for prediction in classes_maladies_predicted 
            if prediction["disease"] in classes_ia_maladies
        ]

        length = len(filtered_predictions)
        filtered_maladies = []

        if length == 0:
            logger.error("Aucune maladie correspondant à l'espèce")
        else:
            highest_prediction = max(filtered_predictions, key=lambda x: x["prediction"])
            filtered_maladies: List[Maladie] = [maladie for maladie in maladies if maladie.classe_ia == highest_prediction["prediction"]]

        return filtered_maladies
        