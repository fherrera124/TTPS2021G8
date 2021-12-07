from sqlalchemy.orm import Session
from app.models import Report, Study
from app.schemas import ReportCreate, ReportUpdate
from app.crud.base import CRUDBase
from typing import Dict, Union, Any
from app.crud.exceptions import StudyAlreadyWithReport



class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def create(
        self, db: Session, study_id: int, obj_in: Union[ReportCreate, Dict[str, Any]]
    ) -> Report:
        if False:  # TODO: implementar
            raise StudyAlreadyWithReport()
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**create_data, study_id=study_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


report = CRUDReport(Report)
