from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas.referring_physician import ReferringPhysicianUpdate, ReferringPhysicianCreate
from app.models.referring_physician import ReferringPhysician
from app.crud.exceptions import *


class CRUDReferringPhysician(CRUDBase[ReferringPhysician, ReferringPhysicianCreate, ReferringPhysicianUpdate]):

    def _validate_update(self, db: Session, db_obj: ReferringPhysician, data: Dict[str, Any]) -> None:
        super()._validate_update(db, db_obj, data)
        if 'email' in data:
            email = data["email"]
            if email and email != db_obj.email:
                user = self.get_by_email(db, email=email)
                if user is not None:
                    raise EmailAlreadyRegistered()
        if 'dni' in data:
            dni = data["dni"]
            if dni and dni != db_obj.dni:
                user = self.get_by_dni(db, dni=dni)
                if user is not None:
                    raise DniAlreadyRegistered()

    def _validate_update(self, db: Session, db_obj: ReferringPhysician, data: Dict[str, Any]) -> None:
        if 'email' in data:
            email = data["email"]
            if email and email != db_obj.email:
                user = self.get_by_email(db, email=email)
                if user is not None:
                    raise EmailAlreadyRegistered()
        if 'username' in data:
            username = data["username"]
            if username and username != db_obj.username:
                user = self.get_by_username(db, username=username)
                if user is not None:
                    raise UsernameAlreadyRegistered()
        if 'license' in data:
            license = data["license"]
            if license and license != db_obj.license:
                existing_user = self.get_by_license(db, license=license)
                if existing_user is not None:
                    raise LicenseAlreadyRegistered()

    def get_by_license(self, db: Session, license: int) -> Optional[ReferringPhysician]:
        return db.query(ReferringPhysician).filter(ReferringPhysician.license == license).first()

    def get_by_email(self, db: Session, email: str) -> Optional[ReferringPhysician]:
        return db.query(ReferringPhysician).filter(ReferringPhysician.email == email).first()

    def update(
            self, db: Session, db_obj: ReferringPhysician, obj_in: Union[ReferringPhysicianUpdate, Dict[str, Any]]
    ) -> ReferringPhysician:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        self._validate_update(db, db_obj=db_obj, data=update_data)
        if 'password' in update_data:
            if update_data["password"]:
                hashed_password = get_password_hash(update_data["password"])
                del update_data["password"]
                update_data["hashed_password"] = hashed_password
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)




        return super().update(db, db_obj=db_obj, obj_in=update_data)


referring_physician = CRUDReferringPhysician(ReferringPhysician)
