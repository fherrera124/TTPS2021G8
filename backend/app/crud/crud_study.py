from typing import List, Optional
from sqlalchemy.sql import func
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import Study, SampleBatch, StudyStates
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
            db=db, db_obj=db_obj, new_state=StudyState.STATE_ONE,
            employee_id=employee_id, entry_date=db_obj.created_date)
        return db_obj

    def get_multi(
        self, db: Session,
        skip: int = 0, limit: int = 100,
        state: Optional[str] = None
    ) -> List[Study]:
        if state is None:
            return db.query(Study).offset(skip).limit(limit).all()
        return db.query(Study).\
            filter(Study.current_state == state).offset(
            skip).limit(limit).all()

    def get_multi_delayed(
        self, db: Session,
        skip: int = 0, limit: int = 100
    ) -> List[Study]:
        return db.query(Study).filter(Study.delayed == True).\
            offset(skip).limit(limit).all()

    def get_multi_by_owner(
        self, db: Session, *, employee_id: int, skip: int = 0, limit: int = 100
    ) -> List[Study]:
        return (
            db.query(Study)
            .filter(Study.employee_id == employee_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_state(self, db: Session, db_obj: Study, new_state: str,
                     employee_id: int, entry_date: Optional[datetime] = None) -> Study:
        if entry_date is None:
            date_time = func.now()
        else:
            date_time = entry_date
        study_new_state = StudyStates(
            study_id=db_obj.id, state=new_state,
            state_entered_date=date_time,
            employee_id=employee_id)
        db.add(study_new_state)
        db_obj.current_state = new_state
        db_obj.updated_date = date_time
        db_obj.current_state_entered_date = date_time
        db.add(db_obj)
        SampleBatch.new_if_qualifies(db_obj=db_obj, db=db)
        db.commit()
        db.refresh(db_obj)
        return db_obj


study = CRUDStudy(Study)
