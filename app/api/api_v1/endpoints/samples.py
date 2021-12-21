from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.crud.exceptions import SampleAlreadyPaid
from app.constants.state import StudyState


router = APIRouter()


def retrieve_sample(db: Session, id: int) -> Optional[models.Sample]:
    sample = crud.sample.get(db=db, id=id)
    if sample is None:
        raise HTTPException(
            status_code=404, detail="No se encontró la muestra."
        )
    return sample


# @router.get("/", response_model=List[schemas.Sample])
# def read_samples(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     paid: Optional[bool] = None,
#     current_user: models.User = Security(
#         deps.get_current_active_user,
#         scopes=[Role.EMPLOYEE["name"]],
#     )
# ) -> Any:
#     """
#     Retrieve samples.
#     """
#     return crud.sample.get_multi(db, paid=paid, skip=skip, limit=limit)


@router.get("/", response_model=List[schemas.Sample])  # temporal fix
def read_unpaid_samples(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Retrieve unpaid samples.
    """
    return crud.sample.get_multi(db, paid=False, skip=skip, limit=limit)


@router.get("/unpaid", response_model=List[schemas.Sample])
def read_unpaid_samples(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Retrieve unpaid samples.
    """
    return crud.sample.get_multi(db, paid=False, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Sample)
def read_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Get sample by ID.
    """
    sample = crud.sample.get(db=db, id=id)
    if not sample:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    return sample


@router.post("/reject-samples")
def reject_samples(
    samples: List[int],
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Reject 1..n samples.
    """
    for sample_id in samples:
        sample = retrieve_sample(db=db, id=sample_id)
        if sample is None:
            raise HTTPException(
                status_code=404, detail="No se encontró la muestra"
            )
        study = sample.study
        if study.current_state == StudyState.STATE_SEVEN:
            crud.sample.remove(db=db, id=sample.id)  # se elimina la muestra
            crud.study.update_state(
                db=db, study=study, new_state=StudyState.STATE_THREE, updated_by_id=current_user.id)
        else:
            raise HTTPException(
                status_code=400, detail="Acción incompatible con el estado del estudio"
            )
    return {"status": "samples successfully rejected and deleted"}


@router.post("/mark-as-processed")
def mark_samples_as_paid(
    samples: List[int],
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mark 1..n samples as processed.
    """
    for sample_id in samples:
        sample = retrieve_sample(db=db, id=sample_id)
        try:
            sample = crud.sample.mark_as_paid(
                db=db, db_obj=sample)
        except SampleAlreadyPaid:
            raise HTTPException(
                status_code=400, detail="La muestra con id: {} ya fue pagada.".format(sample_id)
            )
    return {"status": "ok"}
