from pydantic import BaseModel


class MonthAmount(BaseModel):
    month: str
    amount: int


class TypeAmount(BaseModel):
    study_type: str
    amount: int
