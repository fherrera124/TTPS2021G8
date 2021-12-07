from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from .user import ReportingPhysician



class ResultEnum(str, Enum):
    # PENDING = 'pendiente'
    POSITIVE = 'positivo'
    NEGATIVE = 'negativo'


# Shared properties
class ReportBase(BaseModel):
    result: Optional[ResultEnum] = None
    report: Optional[str]


# Properties to receive on item creation
class ReportCreate(ReportBase):
    result: ResultEnum
    report: str


# Properties to receive on item update
class ReportUpdate(ReportBase):
    pass


# Properties shared by models stored in DB
class ReportInDBBase(ReportBase):
    id: int
    study_id: int
    date_report: Optional[datetime] = None
    reporting_physician: Optional[ReportingPhysician] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Report(ReportInDBBase):
    pass


# Properties properties stored in DB
class ReportInDB(ReportInDBBase):
    pass
