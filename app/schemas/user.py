from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Extra


# Base classes
class UserBase(BaseModel):
    is_active: Optional[bool] = True
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    force_password_change: Optional[bool] = False


class AdminBase(UserBase):
    pass


class ConfigBase(UserBase):
    pass


class EmployeeBase(UserBase):
    pass


class ReportingBase(UserBase):
    license: Optional[int]


class PatientBase(BaseModel):
    is_active: Optional[bool] = True
    first_name: Optional[str]
    last_name: Optional[str]
    first_name_tutor: Optional[str]
    last_name_tutor: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    dni: Optional[int]
    birth_date: Optional[date]
    health_insurance_number: Optional[int]
    health_insurance_id: Optional[int]
    clinical_history: Optional[str]


# Properties to receive via API on creation

class AdminCreate(AdminBase):
    password: str


class ConfigCreate(ConfigBase):
    password: str


class EmployeeCreate(EmployeeBase):
    password: str


class ReportingCreate(ReportingBase):
    license: int
    password: str


class PatientCreate(PatientBase):
    first_name: str
    last_name: str
    first_name_tutor: Optional[str]
    last_name_tutor: Optional[str]
    force_password_change: Optional[bool] = True
    address: str
    phone_number: str
    email: EmailStr
    dni: int
    birth_date: date
    clinical_history: str

    class Config:
        extra = Extra.allow  # para permitir la creacion de campos en la instancia

    def __init__(self, **data):
        super().__init__(**data)
        self.username = str(self.dni)
        self.password = str(self.dni)

# Properties to receive via API on update


class AdminUpdate(AdminBase):
    password: Optional[str] = None


class ConfigUpdate(ConfigBase):
    password: Optional[str] = None


class EmployeeUpdate(EmployeeBase):
    password: Optional[str] = None


class ReportingUpdate(ReportingBase):
    password: Optional[str] = None


class PatientUpdate(PatientBase):
    force_password_change: Optional[bool] = True


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API


class User(UserInDBBase):
    pass


class Administrator(UserInDBBase, AdminBase):
    pass


class Configurator(UserInDBBase, ConfigBase):
    pass


class Employee(UserInDBBase, EmployeeBase):
    pass


class ReportingPhysician(UserInDBBase, ReportingBase):
    pass


class Patient(UserInDBBase, PatientBase):
    pass


# Additional properties stored in DB
class AdminInDB(UserInDBBase, AdminBase):
    hashed_password: str


class ConfigInDB(UserInDBBase, ConfigBase):
    hashed_password: str


class EmployeeInDB(UserInDBBase, EmployeeBase):
    hashed_password: str


class ReportingInDB(UserInDBBase, ReportingBase):
    hashed_password: str


class PatientInDB(UserInDBBase, PatientBase):
    hashed_password: str
