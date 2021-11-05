from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.constants.role import Role
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType
from app.models import User, Admin, Employee, ReportingPhysician, Patient, UserRole
from app.schemas import (
    AdminCreate, AdminUpdate,
    ReportingCreate, ReportingUpdate,
    EmployeeCreate, EmployeeUpdate,
    PatientCreate, PatientUpdate
)
from app import crud


class FastAPIUsersException(Exception):
    pass


class UserAlreadyExists(FastAPIUsersException):
    pass


class UsernameAlreadyRegistered(FastAPIUsersException):
    pass


class EmailAlreadyRegistered(FastAPIUsersException):
    pass


class DniAlreadyRegistered(FastAPIUsersException):
    pass


class LicenseAlreadyRegistered(FastAPIUsersException):
    pass


class UserNotExists(FastAPIUsersException):
    pass


class UserInactive(FastAPIUsersException):
    pass


class CRUDUser(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def _validate_creation(self, db: Session, data: Dict[str, Any]) -> None:
        existing_user = self.get_by_username(db, username=data["username"])
        if existing_user is not None:
            raise UsernameAlreadyRegistered()

    def _get_role_obj(self, db: Session):
        # definido en las subclases
        pass

    def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)
        self._validate_creation(db, create_data)

        del create_data["password"]
        create_data["hashed_password"] = get_password_hash(obj_in.password)

        db_obj = self.model(**create_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        # asignación de rol al usuario recien creado
        role_obj = self._get_role_obj(db=db)
        user_role = UserRole(user_id=db_obj.id, role_id=role_obj.id)
        db.add(user_role)
        db.commit()

        return db_obj

    def _validate_update(self, db: Session, db_obj: ModelType, data: Dict[str, Any]) -> None:
        username = data["username"]
        if username and username != db_obj.username:
            user = self.get_by_username(db, username)
            if user is not None:
                raise UsernameAlreadyRegistered()

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        self._validate_update(db, db_obj, update_data)

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj, obj_in)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[ModelType]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: ModelType) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.type == 'admin'

    def is_employee(self, user: User) -> bool:
        return user.type == 'employee'

    def is_reporting_physician(self, user: User) -> bool:
        return user.type == 'reportingphysician'

    def type(self, user: User) -> str:
        return user.type


class CRUDReportingPhysician(CRUDUser[ReportingPhysician, ReportingCreate, ReportingUpdate]):
    def _validate_creation(self, db: Session, data: Dict[str, Any]) -> None:
        super()._validate_creation(db, data)
        existing_user = self.get_by_license(db, license=data["license"])
        if existing_user is not None:
            raise LicenseAlreadyRegistered()

    def _validate_update(self, db: Session, db_obj: ReportingPhysician, data: Dict[str, Any]) -> None:
        super()._validate_update(db, db_obj, data)
        license = data["license"]
        if license and license != db_obj.license:
            try:
                self._get_by_license(db, license=license)
                raise LicenseAlreadyRegistered()
            except UserNotExists:
                pass

    def get_by_license(self, db: Session, *, email: str) -> Optional[ModelType]:
        if hasattr(self.model, 'license'):
            return db.query(self.model).filter(self.model.license == license).first()
    
    def _get_role_obj(self, db: Session):
        return crud.role.get_by_name(db=db, name=Role.REPORTING_PHYSICIAN["name"])


class CRUDEmployee(CRUDUser[Employee, EmployeeCreate, EmployeeUpdate]):
    def _get_role_obj(self, db: Session):
        return crud.role.get_by_name(db=db, name=Role.EMPLOYEE["name"])


class CRUDAdmin(CRUDUser[Admin, AdminCreate, AdminUpdate]):
    def _get_role_obj(self, db: Session):
        return crud.role.get_by_name(db=db, name=Role.ADMIN["name"])


class CRUDPatient(CRUDUser[Patient, PatientCreate, PatientUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[ModelType]:
        return db.query(Patient).filter(Patient.email == email).first()

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[ModelType]:
        return db.query(Patient).filter(Patient.dni == dni).first()

    def _validate_creation(self, db: Session, data: Dict[str, Any]) -> None:
        super()._validate_creation(db, data)
        existing_user = self.get_by_email(db, email=data["email"])
        if existing_user is not None:
            raise EmailAlreadyRegistered()
        existing_user = self.get_by_dni(db, dni=data["dni"])
        if existing_user is not None:
            raise DniAlreadyRegistered()

    def _validate_update(self, db: Session, db_obj: Patient, data: Dict[str, Any]) -> None:
        super()._validate_update(db, db_obj, data)
        email = data["email"]
        if email and email != db_obj.email:
            user = self.get_by_email(db, email=email)
            if user is not None:
                raise EmailAlreadyRegistered()
        dni = data["dni"]
        if dni and dni != db_obj.dni:
            user = self.get_by_dni(db, dni=dni)
            if user is not None:
                raise DniAlreadyRegistered()

    def _get_role_obj(self, db: Session):
        return crud.role.get_by_name(db=db, name=Role.PATIENT["name"])


admin = CRUDAdmin(Admin)

user = CRUDUser(User)

employee = CRUDEmployee(Employee)

reporting_physician = CRUDReportingPhysician(ReportingPhysician)

patient = CRUDPatient(Patient)
