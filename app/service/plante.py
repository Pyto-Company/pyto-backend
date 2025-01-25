from app.repository.entretien import EntretienRepository
from app.repository.rappel import RappelRepository
from app.repository.scan import ScanRepository
from app.dto.InscriptionDTO import InscriptionEmailDTO
from app.model.utilisateur import ProviderType
from sqlalchemy.ext.asyncio import AsyncSession

class PlanteService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getEntretiensPrincipaux(self, espece_id: int):
        return await EntretienRepository(self.session).get_entretiens_by_espece_id(espece_id)
    