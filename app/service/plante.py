from repository.entretien import EntretienRepository
from repository.rappel import RappelRepository
from repository.scan import ScanRepository
from dto.InscriptionDTO import InscriptionEmailDTO
from model.utilisateur import ProviderType
from sqlalchemy.ext.asyncio import AsyncSession

class PlanteService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getEntretiensPrincipaux(self, espece_id: int):
        return await EntretienRepository(self.session).get_entretiens_by_espece_id(espece_id)
    