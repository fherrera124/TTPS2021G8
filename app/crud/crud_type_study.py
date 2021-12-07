from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas.study import TypeStudyUpdate, TypeStudyCreate
from app.models import TypeStudy


class CRUDTypeStudy(CRUDBase[TypeStudy, TypeStudyCreate, TypeStudyUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[TypeStudy]:
        return db.query(TypeStudy).filter(TypeStudy.name == name).first()

    def create(self, db: Session, *, obj_in: TypeStudyCreate) -> TypeStudy:
        db_obj = TypeStudy(
            name=obj_in.name,
            study_consent_template=obj_in.study_consent_template
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: TypeStudy, obj_in: Union[TypeStudyUpdate, Dict[str, Any]]
    ) -> TypeStudy:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_template(self, db: Session, db_obj: TypeStudy, template: str) -> TypeStudy:
        db_obj.study_consent_template = template
        db.commit()
        db.refresh(db_obj)
        return db_obj


type_study = CRUDTypeStudy(TypeStudy)
