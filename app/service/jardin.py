from dto.plante_jardin import PlanteJardinDTO
from typing import List
from repository.jardin import JardinRepository
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session

class JardinService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = JardinRepository(session)

    async def get(self, user_id: int) -> List[PlanteJardinDTO]:
        return await self.repository.get_jardin(user_id)
