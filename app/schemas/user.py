from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr


# Base classes
class UserBase(BaseModel):
    is_active: Optional[bool] = True
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class AdminBase(UserBase):
    pass


class ConfigBase(UserBase):
    pass


class EmployeeBase(UserBase):
    pass


class ReportingBase(UserBase):
    license: Optional[int]


class PatientBase(UserBase):
    email: Optional[EmailStr]
    dni: Optional[str]
    birth_date: Optional[date]
    health_insurance_number: Optional[int]
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
    username: str
    password: str
    email: EmailStr
    dni: int
    birth_date: date
    health_insurance_number: int
    clinical_history: str


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
    password: Optional[str] = None


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
