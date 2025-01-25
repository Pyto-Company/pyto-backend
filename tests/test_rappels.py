import pytest
from datetime import datetime
from app.repository.rappel import RappelRepository
from sqlalchemy.orm import Session

@pytest.mark.asyncio
def test_rappels(session: Session) -> None:
    results = RappelRepository(session).get_rappels_by_user_id(1)
    print(results)
    assert len(results) == 8
    assert results[0].id_rappel == 2
    assert results[0].date_prochain_rappel == datetime(2025, 1, 26, 12, 30)
    assert results[1].id_rappel == 5
    assert results[1].date_prochain_rappel == datetime(2025, 1, 27, 12, 30)
    assert results[2].id_rappel == 7
    assert results[2].date_prochain_rappel == datetime(2025, 1, 27, 12, 30)
    assert results[3].id_rappel == 3
    assert results[3].date_prochain_rappel == datetime(2025, 1, 28, 12, 30)
    assert results[4].id_rappel == 1
    assert results[4].date_prochain_rappel == datetime(2025, 1, 29, 12, 30)
    assert results[5].id_rappel == 6
    assert results[5].date_prochain_rappel == datetime(2025, 1, 30, 12, 30)
    assert results[6].id_rappel == 4
    assert results[6].date_prochain_rappel == datetime(2025, 1, 30, 12, 30)
    assert results[7].id_rappel == 8
    assert results[7].date_prochain_rappel == datetime(2025, 1, 31, 12, 30)