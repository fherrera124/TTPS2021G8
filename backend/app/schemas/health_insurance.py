from typing import List, Optional
<<<<<<< HEAD
from app.schemas import Patient
=======
from app.schemas.user import User #TODO: que sea paciente
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
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
<<<<<<< HEAD
    affiliates: List[Patient] = []
=======
    affiliates: List[User] = []
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3

    class Config:
        orm_mode = True


# Properties to return to client
class HealthInsurance(HealthInsuranceInDBBase):
    pass


# Properties properties stored in DB
class HealthInsuranceInDB(HealthInsuranceInDBBase):
    pass