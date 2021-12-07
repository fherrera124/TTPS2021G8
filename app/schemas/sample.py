from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    study_id: int
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
