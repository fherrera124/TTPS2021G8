from typing import List, Optional
from sqlalchemy.sql import func, extract
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import Study, TypeStudy, SampleBatch, StudyStates
from app.schemas import StudyCreate, StudyUpdate
from app.constants.state import StudyState
from datetime import datetime


class CRUDStudy(CRUDBase[Study, StudyCreate, StudyUpdate]):
    def create(
        self, db: Session, *, obj_in: StudyCreate, employee_id: int
    ) -> Study:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, employee_id=employee_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        self.update_state(
            db=db, study=db_obj, new_state=StudyState.STATE_ONE,
            updated_by_id=employee_id, entry_date=db_obj.created_date)
        return db_obj

    def get_multi(
        self, db: Session,
        skip: int = 0, limit: int = 100,
        state: Optional[str] = None,
        patient_id: Optional[int] = None
    ) -> List[Study]:
        res = db.query(Study)
        if patient_id:
            res = res.filter(Study.patient_id == patient_id)
        if state:
            res = res.filter(Study.current_state == state)
        return res.offset(skip).limit(limit).all()

    def get_multi_delayed(
        self, db: Session,
        skip: int = 0, limit: int = 100
    ) -> List[Study]:
        return db.query(Study).filter(Study.delayed == True).\
            offset(skip).limit(limit).all()

    def get_multi_by_owner(
        self, db: Session, *, employee_id: int,
        skip: int = 0, limit: int = 100
    ) -> List[Study]:
        return (
            db.query(Study)
            .filter(Study.employee_id == employee_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_month_amount(
        self, db: Session,
        month: int
    ) -> int:
        return db.query(Study).filter(extract('month', Study.created_date) == month).count()

    def get_type_amount(
        self, db: Session,
        study_type: str
    ) -> int:
        return db.query(Study).join(TypeStudy).filter(TypeStudy.name == study_type).count()

    def mark_delayed(self, db: Session, db_obj: Study) -> Study:
        db_obj.delayed = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_state(self, db: Session, study: Study, new_state: str,
                     updated_by_id: int, entry_date: Optional[datetime] = None) -> Study:
        if entry_date is None:
            date_time = func.now()
        else:
            date_time = entry_date
        study_new_state = StudyStates(
            study_id=study.id, state=new_state,
            state_entered_date=date_time,
            updated_by_id=updated_by_id)
        db.add(study_new_state)
        study.current_state = new_state
        study.updated_date = date_time
        study.current_state_entered_date = date_time
        db.add(study)
        sample_batch = SampleBatch.new_if_qualifies(study=study, db=db)
        if sample_batch:  # se creo un lote
            for sample in sample_batch.samples:
                study_new_state = StudyStates(
                    study_id=sample.study.id, state=StudyState.STATE_SEVEN,
                    state_entered_date=date_time,
                    updated_by_id=updated_by_id)
                db.add(study_new_state)
        db.commit()
        db.refresh(study)
        return study


study = CRUDStudy(Study)
