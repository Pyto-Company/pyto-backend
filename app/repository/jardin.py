from fastapi import Depends, Query, HTTPException
from sqlmodel import Session, select
from app.database.database import get_session, engine
from sqlalchemy import text
from app.dto.plante_jardin import PlanteJardinDTO
from typing import List

class JardinRepository():

    def get_jardin(user_id: int) -> List[PlanteJardinDTO]:
        with Session(engine) as session:
            sql = text("SELECT p.id, p.nom, e.nom_commun, e.photo_defaut \
                    FROM plante p \
                    INNER JOIN espece e on e.id = p.espece_id \
                    WHERE p.utilisateur_id = :param1")
            
            result = session.execute(sql, {"param1": user_id}).fetchall()
            
            # Convert the result to a list of dictionaries
            return [{"id_plante": row[0], "nom_plante": row[1], "nom_commun_espece": row[2], "nom_fichier": row[3]} for row in result]
