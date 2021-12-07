from sqlalchemy.orm import Session
from app.models import Sample, Study
from app.schemas import SampleCreate, SampleUpdate
from app.crud.base import CRUDBase
from typing import Dict, Union, Any, Optional, List
from app.crud.exceptions import StudyAlreadyWithSample, SampleAlreadyPickedUp, SampleAlreadyPaid
from sqlalchemy.sql import func


class CRUDSample(CRUDBase[Sample, SampleCreate, SampleUpdate]):
    def create(
        self, db: Session, study_id: int, obj_in: Union[SampleCreate, Dict[str, Any]]
    ) -> Sample:
        if 1 == 2:  # TODO: implementar
            raise StudyAlreadyWithSample()
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**create_data, study_id=study_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def register_extractionist(self, db: Session, db_obj: Sample, picked_up_by: str) -> Optional[Sample]:
        if db_obj.picked_up_by is not None:
            raise SampleAlreadyPickedUp()
        db_obj.picked_up_by = picked_up_by
        db_obj.picked_up_date = func.now()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def mark_as_paid(
            self, db: Session, db_obj: Sample) -> Optional[Sample]:
        if db_obj.paid is not None and db_obj.paid is True:
            raise SampleAlreadyPaid()
        db_obj.paid = True
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, paid: Optional[bool] = None, skip: int = 0, limit: int = 100
    ) -> List[Sample]:
        if paid is None:
            samples = super().get_multi(db, skip=skip, limit=limit)
        else:
            samples = db.query(Sample).filter(Sample.paid == paid).offset(skip).limit(limit).all()
        return samples


sample = CRUDSample(Sample)
