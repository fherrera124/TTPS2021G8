from typing import List, Optional
from app.schemas import Patient
from pydantic import BaseModel


# Shared properties
class HealthInsuranceBase(BaseModel):
    name: str
    telephone: str
    email: str


# Properties to receive on item creation
class HealthInsuranceCreate(HealthInsuranceBase):
    pass


# Properties to receive on item update
class HealthInsuranceUpdate(HealthInsuranceBase):
    pass


# Properties shared by models stored in DB
class HealthInsuranceInDBBase(HealthInsuranceBase):
    id: int
    affiliates: List[Patient] = []

    class Config:
        orm_mode = True


# Properties to return to client
class HealthInsurance(HealthInsuranceInDBBase):
    pass


# Properties properties stored in DB
class HealthInsuranceInDB(HealthInsuranceInDBBase):
    pass