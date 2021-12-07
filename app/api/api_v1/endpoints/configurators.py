from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app.crud import UsernameAlreadyRegistered
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from app.constants.role import Role

router = APIRouter()


@router.get("/", response_model=List[schemas.Configurator])
def read_configurators(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve configurators.
    """
    configurators = crud.config.get_multi(db, skip=skip, limit=limit)
    return configurators


@router.post("/", response_model=schemas.Configurator)
def create_configurator(
    *,
    db: Session = Depends(deps.get_db),
    configurator_in: schemas.ConfigCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Create new configurator.
    """
    try:
        configurator = crud.config.create(db, obj_in=configurator_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
    return configurator


@router.get("/{configurator_id}", response_model=schemas.Configurator)
def read_configurator_by_id(
    configurator_id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.CONFIGURATOR["name"]],
    ),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific configurator by id.
    """
    configurator = crud.config.get(db, id=configurator_id)
    if not configurator:
        raise HTTPException(
            status_code=404,
            detail="El configurador con el id ingresado no existe en el sistema",
        )
    if crud.user.is_admin(current_user):
        return configurator
    if configurator != current_user:
        raise HTTPException(
            status_code=401, detail="Usted no tiene los permisos suficientes"
        )
    return configurator


@router.put("/{configurator_id}", response_model=schemas.Configurator)
def update_configurator(
    *,
    db: Session = Depends(deps.get_db),
    configurator_id: int,
    configurator_in: schemas.ConfigUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> Any:
    """
    Update a configurator.
    """
    configurator = crud.config.get(db, id=configurator_id)
    if not configurator:
        raise HTTPException(
            status_code=404,
            detail="El configurador con el id ingresado no existe en el sistema",
        )
    try:
        return crud.config.update(db, db_obj=configurator, obj_in=configurator_in)
    except UsernameAlreadyRegistered:
        raise HTTPException(
            status_code=400,
            detail="El username ingresado ya se encuentra registrado",
        )
