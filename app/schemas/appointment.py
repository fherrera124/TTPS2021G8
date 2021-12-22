from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Shared properties
class AppointmentBase(BaseModel):
    date_appointment: Optional[datetime] = None
    description: Optional[str] = None


# Properties to receive on item creation
class AppointmentCreate(AppointmentBase):
    date_appointment: datetime
    description: str


# Properties to receive on item update
class AppointmentUpdate(AppointmentBase):
    current_state: Optional[str] = None


# Properties shared by models stored in DB
class AppointmentInDBBase(AppointmentBase):
    id: int
    study_id: int
    current_state: Optional[str] = None #no deberia ser opcional, pero para que no rompa mientras no actualice la db

    class Config:
        orm_mode = True


# Properties to return to client
class Appointment(AppointmentInDBBase):
    pass


class AppointmentSimplified(BaseModel):
    start: str
    end: str
    patient: dict = None


# Properties properties stored in DB
class AppointmentInDB(AppointmentInDBBase):
    pass
