from sqlalchemy.orm import Session
from app.models import HealthInsurance
from app.schemas import HealthInsuranceCreate, HealthInsuranceUpdate
from app.crud.base import CRUDBase
from typing import Dict, Any, Union, Optional
from app.crud.exceptions import NameAlreadyRegistered, EmailAlreadyRegistered


class CRUDHealthInsurance(CRUDBase[HealthInsurance, HealthInsuranceCreate, HealthInsuranceUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[HealthInsurance]:
        return db.query(HealthInsurance).filter(HealthInsurance.name == name).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[HealthInsurance]:
        return db.query(HealthInsurance).filter(HealthInsurance.email == email).first()

    def create(
        self, db: Session, *, obj_in: Union[HealthInsuranceCreate, Dict[str, Any]]
    ) -> HealthInsurance:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)
        health_insurance = self.get_by_name(db, name=data["name"])
        if health_insurance is not None:
            raise NameAlreadyRegistered()
        health_insurance = self.get_by_email(db, email=data["email"])
        if health_insurance is not None:
            raise EmailAlreadyRegistered()
        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _validate_update(self, db: Session, db_obj: HealthInsurance, data: Dict[str, Any]) -> None:
        if 'name' in data:
            name = data["name"]
            if name and name != db_obj.name:
                user = self.get_by_name(db, name=name)
                if user is not None:
                    raise NameAlreadyRegistered()
        if 'email' in data:
            email = data["email"]
            if email and email != db_obj.email:
                user = self.get_by_email(db, email=email)
                if user is not None:
                    raise EmailAlreadyRegistered()

    def update(
        self, db: Session, *, db_obj: HealthInsurance, obj_in: Union[HealthInsuranceUpdate, Dict[str, Any]]
    ) -> HealthInsurance:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        self._validate_update(db, db_obj=db_obj, data=update_data)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


health_insurance = CRUDHealthInsurance(HealthInsurance)
