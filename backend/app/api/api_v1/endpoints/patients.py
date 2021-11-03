from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.crud.crud_user import (
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered
)
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.Patient])
def read_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.Patient = Depends(deps.get_current_if_admin),
) -> Any:
    """
    Retrieve patients.
    """
    patients = crud.patient.get_multi(db, skip=skip, limit=limit)
    return patients


@router.post("/", response_model=schemas.Patient)
def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: schemas.PatientCreate,
    current_user: models.Patient = Depends(deps.get_current_if_admin),
) -> Any:
    """
    Create new patient.
    """
    try:
        patient = crud.patient.create(db, obj_in=patient_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
    if settings.EMAILS_ENABLED and patient_in.email:
        send_new_account_email(
            email_to=patient_in.email, username=patient_in.username, password=patient_in.password
        )
    return patient


@router.post("/open", response_model=schemas.Patient)
def create_patient_open(
    *,
    db: Session = Depends(deps.get_db),
    first_name: str = Body(...),
    last_name: str = Body(...),
    password: str = Body(...),
    email: EmailStr = Body(...)
    
) -> Any:
    """
    Create new patient without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open users registration is forbidden on this server",
        )
    patient_in = schemas.PatientCreate(
        password=password, first_name=first_name, last_name=last_name)
    try:
        patient = crud.patient.create(db, obj_in=patient_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
    return patient


@router.get("/{patient_id}", response_model=schemas.Patient)
def read_patient_by_id(
    patient_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific patient by id.
    """
    patient = crud.patient.get(db, id=patient_id)
    if patient == current_user:
        return patient
    if not crud.user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return patient


@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    patient_in: schemas.PatientUpdate,
    current_user: models.User = Depends(deps.get_current_if_admin),
) -> Any:
    """
    Update a patient.
    """
    patient = crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="The patient with this id does not exist in the system",
        )
    try:
        return crud.patient.update(db, db_obj=patient, obj_in=patient_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=404,
            detail="El username ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=404,
            detail="El email ingresado ya se encuentra registrado",
        )
