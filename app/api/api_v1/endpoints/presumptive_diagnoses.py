
from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Diagnosis
from app.api import deps
from pydantic import BaseModel


router = APIRouter()


class PresumptiveDiagnosis(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True


# TODO: manejar por roles
@router.get("/", response_model=List[PresumptiveDiagnosis])
def read_presumptive_diagnoses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve presumptive diagnoses.
    """
    return db.query(Diagnosis).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=PresumptiveDiagnosis)
def read_by_id(
    presumptive_diagnosis_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific presumptive_diagnosis by id.
    """
    return db.query(Diagnosis).filter(Diagnosis.id == presumptive_diagnosis_id).first()