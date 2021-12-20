from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime, date


class SimplifiedPatient(BaseModel):
    id: int
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

    class Config:
        orm_mode = True


class SimplifiedTypeStudy(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SimplifiedStudy(BaseModel):
    id: int
    current_state: Optional[str] = None
    type_study: Optional[SimplifiedTypeStudy] = None
    patient: Optional[SimplifiedPatient] = None

    class Config:
        orm_mode = True


# Shared properties
class SampleBase(BaseModel):
    ml_extracted: Optional[float] = None
    freezer_number: Optional[int] = None


# Properties to receive on item creation
class SampleCreate(SampleBase):
    ml_extracted: float
    freezer_number: int


# Properties to receive on item update
class SampleUpdate(SampleBase):
    pass


# Properties shared by models stored in DB
class SampleInDBBase(SampleBase):
    id: int
    study: Optional[SimplifiedStudy] = None
    ml_extracted: Optional[float] = None
    freezer_number: Optional[int] = None
    picked_up_by: Optional[str] = None
    picked_up_date: Optional[datetime] = None
    sample_batch_id: Optional[int] = None
    #sample_batch = Optional[SampleBatch] = None
    paid: Optional[bool] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Sample(SampleInDBBase):
    pass
