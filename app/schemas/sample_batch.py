from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from .sample import Sample


# Shared properties
class SampleBatchBase(BaseModel):
    pass


# Properties to receive on item creation
class SampleBatchCreate(SampleBatchBase):
    pass


# Properties to receive on item update
class SampleBatchUpdate(SampleBatchBase):
    pass


# Properties shared by models stored in DB
class SampleBatchInDBBase(SampleBatchBase):
    id: int
    created_date: Optional[datetime] = None
    current_state: Optional[str] = None
    samples: Optional[List[Sample]] = None

    class Config:
        orm_mode = True


# Properties to return to client
class SampleBatch(SampleBatchInDBBase):
    pass


# Properties properties stored in DB
class SampleBatchInDB(SampleBatchInDBBase):
    pass
