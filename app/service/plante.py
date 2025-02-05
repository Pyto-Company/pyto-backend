from app.repository.entretien import EntretienRepository
from sqlalchemy.orm import Session

class PlanteService:

    def __init__(self, session: Session):
        self.session = session
    
    def getEntretiensPrincipaux(self, espece_id: int):
        return EntretienRepository(self.session).get_entretiens_by_espece_id(espece_id)
    