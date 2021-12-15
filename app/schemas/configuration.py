from pydantic import BaseModel
from datetime import datetime


# Shared properties
class ConfigurationBase(BaseModel):
    obligated_mode: bool


# Properties to receive on item creation
class ConfigurationCreate(ConfigurationBase):
    pass


# Properties to receive on item update
class ConfigurationUpdate(ConfigurationBase):
    pass


# Properties shared by models stored in DB
class ConfigurationInDBBase(ConfigurationBase):
    id: int
    updated_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Configuration(ConfigurationInDBBase):
    pass


# Properties properties stored in DB
class ConfigurationInDB(ConfigurationInDBBase):
    pass
