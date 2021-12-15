from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.crud import (
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered,
    DniAlreadyRegistered,
    TutorDataMissing
)
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from app.constants.role import Role

router = APIRouter()


@router.get("/", response_model=List[schemas.Patient])
def read_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
) -> Any:
    """
    Retrieve patients.
    """
    patients = crud.patient.get_multi(db, skip=skip, limit=limit)
    return patients


@router.post("/", response_model=schemas.Patient)
async def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: schemas.PatientCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
) -> Any:
    """
    Create new patient.
    """
    #TODO: estaria bueno que se valide en caso de ser menor, que los campos de
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
    except DniAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El dni ingresado ya se encuentra registrado",
        )
    except TutorDataMissing:
        raise HTTPException(
            status_code=400,
            detail="Paciente menor de 18 requiere nombre y apellido del tutor",
        )
    #if settings.EMAILS_ENABLED and patient_in.email: FIXME (no me toma el EMAILS_ENABLED=True en .env)
    print(settings.EMAILS_ENABLED)
    print(patient_in.email)
    await send_new_account_email(
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
        return crud.patient.create(db, obj_in=patient_in)
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
    except DniAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El dni ingresado ya se encuentra registrado",
        )


@router.get("/{patient_id}", response_model=schemas.Patient)
def read_patient_by_id(
    patient_id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.PATIENT["name"]],
    ),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific patient by id.
    """
    patient = crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="El paciente con el id ingresado no existe en el sistema",
        )
    if crud.user.is_employee(current_user):
        return patient
    if patient != current_user:
        raise HTTPException(
            status_code=401, detail="Usted no tiene los permisos suficientes"
        )
    return patient


@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
    patient_in: schemas.PatientUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
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
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
    except DniAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El dni ingresado ya se encuentra registrado",
        )
