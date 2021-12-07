from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas.study import StudyStateUpdate, StudyStateCreate
from app.models import StudyStates


class CRUDStudyStates(CRUDBase[StudyStates, StudyStateCreate, StudyStateUpdate]):
    def get_multi_by_study(
        self, db: Session, study_id: int
    ) -> List[StudyStates]:
        return (
            db.query(StudyStates)
            .filter(Study.study_id == study_id)
            .all()
        )


study_states = CRUDStudyStates(StudyStates)
