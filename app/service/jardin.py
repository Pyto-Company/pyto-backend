from app.dto.plante_jardin import PlanteJardinDTO
from typing import List

from app.repository.jardin import JardinRepository

class JardinService():

    def get(user_id: int) -> List[PlanteJardinDTO]:
        return JardinRepository.get_jardin(user_id)
