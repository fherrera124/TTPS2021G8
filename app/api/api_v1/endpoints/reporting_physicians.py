from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.crud.crud_user import (
    UsernameAlreadyRegistered,
    LicenseAlreadyRegistered
)
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=List[schemas.ReportingPhysician])
def read_reporting_physicians(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
) -> Any:
    """
    Retrieve reporting physicians.
    """
    reportings = crud.reporting_physician.get_multi(db, skip=skip, limit=limit)
    return reportings


@router.post("/", response_model=schemas.ReportingPhysician)
def create_reporting_physician(
    *,
    db: Session = Depends(deps.get_db),
    reporting_in: schemas.ReportingCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    )
) -> Any:
    """
    Create new reporting physician.
    """
    try:
        return crud.reporting_physician.create(db, obj_in=reporting_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except LicenseAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="La licencia ingresada ya se encuentra registrada",
        )


@router.get("/{reporting_id}", response_model=schemas.ReportingPhysician)
def read_reporting_physician_by_id(
    reporting_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific employee by id.
    """
    reporting = crud.reporting_physician.get(db, id=reporting_id)
    if not reporting:
        raise HTTPException(
            status_code=404,
            detail="El médico informante con el id ingresado no existe en el sistema",
        )
    if crud.user.is_admin(current_user):
        return reporting
    if reporting != current_user:
        raise HTTPException(
            status_code=401, detail="Usted no tiene los permisos suficientes"
        )
    return reporting


@router.put("/{reporting_id}", response_model=schemas.ReportingPhysician)
def update_reporting_physician(
    *,
    db: Session = Depends(deps.get_db),
    reporting_id: int,
    reporting_in: schemas.ReportingUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    )
) -> Any:
    """
    Update a reporting physician.
    """
    reporting = crud.reporting_physician.get(db, id=reporting_id)
    if not reporting:
        raise HTTPException(
            status_code=404,
            detail="La id ingresada no corresponde a ningún médico informante registrado en el sistema",
        )
    try:
        return crud.reporting_physician.update(
            db, db_obj=reporting, obj_in=reporting_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except LicenseAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="La licencia ingresada ya se encuentra registrada",
        )
