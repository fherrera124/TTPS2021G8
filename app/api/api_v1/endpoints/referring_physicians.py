from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.crud.crud_user import (
    UsernameAlreadyRegistered,
    LicenseAlreadyRegistered,
    EmailAlreadyRegistered
)


router = APIRouter()


@router.get("/", response_model=List[schemas.ReferringPhysician])
def read_referring_physician(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve referring physician.
    """
    referring_physician = crud.referring_physician.get_multi(db, skip=skip, limit=limit)
    return referring_physician


@router.post("/", response_model=schemas.ReferringPhysician)
def create_referring_physician(
        *,
        db: Session = Depends(deps.get_db),
        referring_physician_in: schemas.ReferringPhysicianCreate,
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Create new referring physician.
    """
    referring_physician = crud.referring_physician.get_by_license(db, license=referring_physician_in.license)
    if referring_physician:
        raise HTTPException(
            status_code=400,
            detail="The referring physician with this license already exists in the system.",
        )
    referring_physician = crud.referring_physician.create(db, obj_in=referring_physician_in)
    return referring_physician


@router.get("/{referring_physician_id}", response_model=schemas.ReferringPhysician)
def read_referring_physician_by_id(
        referring_physician_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Get a referring physician user by id.
    """
    referring_physician = crud.referring_physician.get(db, id=referring_physician_id)
    if not referring_physician:
        raise HTTPException(
            status_code=400,
            detail="The referring physician with this id does not exists in the system.",
        )
    return referring_physician


@router.put("/{referring_physician_id}", response_model=schemas.ReferringPhysician)
def update_referring_physician(
        *,
        db: Session = Depends(deps.get_db),
        referring_physician_id: int,
        referring_physician_in: schemas.ReferringPhysicianUpdate,
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Update a referring physician.
    """
    physician = crud.referring_physician.get(db, id=referring_physician_id)
    if not physician:
        raise HTTPException(
            status_code=404,
            detail="La id ingresada no corresponde a ningún médico derivante registrado en el sistema",
        )
    try:
        return crud.referring_physician.update(db, db_obj=physician, obj_in=referring_physician_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    except LicenseAlreadyRegistered: #TODO: cruzar con las licencias de un medico informante, o no?
        raise HTTPException(
            status_code=400,
            detail="La licencia ingresada ya se encuentra registrada",
        )
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El email ingresado ya se encuentra registrado",
        )
