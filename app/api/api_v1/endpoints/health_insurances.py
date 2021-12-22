from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.crud import NameAlreadyRegistered, EmailAlreadyRegistered


router = APIRouter()


def retrieve_health_insurance(db: Session, id: int) -> Optional[models.HealthInsurance]:
    health_insurance = crud.health_insurance.get(db=db, id=id)
    if health_insurance is None:
        raise HTTPException(
            status_code=404, detail="No se encontró la obra social."
        )
    return health_insurance


@router.get("/", response_model=List[schemas.HealthInsurance])
def read_health_insurances(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.CONFIGURATOR["name"]],
    )
) -> Any:
    """
    Retrieve health insurances.
    """
    return crud.health_insurance.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.HealthInsurance)
def read_health_insurance(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.CONFIGURATOR["name"]]
    )
) -> Any:
    """
    Get health insurance by ID.
    """
    health_insurance = retrieve_health_insurance(db=db, id=id)
    return health_insurance


@router.post("/", response_model=schemas.HealthInsurance)
def create_health_insurance(
    *,
    db: Session = Depends(deps.get_db),
    health_insurance_in: schemas.HealthInsuranceCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.CONFIGURATOR["name"]],
    )
) -> Any:
    """
    Create new health insurance.
    """
    try:
        health_insurance = crud.health_insurance.create(
            db=db, obj_in=health_insurance_in)
    except NameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El nombre ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
    return health_insurance


@router.put("/{id}", response_model=schemas.HealthInsurance)
def update_health_insurance(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    health_insurance_in: schemas.HealthInsuranceUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.CONFIGURATOR["name"]],
    ),
) -> Any:
    """
    Update a health insurance.
    """
    health_insurance = retrieve_health_insurance(db=db, id=id)
    try:
        return crud.health_insurance.update(db, db_obj=health_insurance, obj_in=health_insurance_in)
    except NameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El nombre ingresado ya se encuentra registrado",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
