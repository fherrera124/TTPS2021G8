from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role


router = APIRouter()


def retrieve_health_insurance(db: Session, id: int) -> Optional[models.HealthInsurance]:
    health_insurance = crud.health_insurance.get(db=db, id=id)
    if health_insurance is None:
        raise HTTPException(
            status_code=404, detail="No se encontró la muestra."
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

# TODO: implementar endpoints de alta y modificación
