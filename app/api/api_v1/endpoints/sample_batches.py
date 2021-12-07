from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.constants.state import StudyState, SampleBatchState
from app.crud.exceptions import SampleBatchAlreadyProccesed


router = APIRouter()


def retrieve_sample_batch(db: Session, id: int, expected_state: Optional[str] = None) -> Optional[models.SampleBatch]:
    sample_batch = crud.sample_batch.get(db=db, id=id)
    if sample_batch is None:
        raise HTTPException(
            status_code=404, detail="No se encontró el lote"
        )
    if expected_state is None or expected_state == sample_batch.current_state:
        return sample_batch
    raise HTTPException(
        status_code=400, detail="Acción incompatible con el estado del lote"
    )


@router.get("/", response_model=List[schemas.SampleBatch])
def read_batches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Retrieve batches.
    """
    if True:  # crud.user.is_admin(current_user):
        batches = crud.sample_batch.get_multi(db, skip=skip, limit=limit)
    else:
        batches = crud.sample_batch.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return batches


@router.get("/{id}", response_model=schemas.SampleBatch)
def read_batch(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Get batch by ID.
    """
    batch = crud.batch.get(db=db, id=id)
    if not batch:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return batch


@router.post("/{id}/mark-as-processed", response_model=schemas.SampleBatch)
def mark_batch_as_processed(
    id: int,
    url: str = Body(...),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    sample_batch = retrieve_sample_batch(
        db, id, expected_state=SampleBatchState.STATE_ONE)
    try:
        sample_batch = crud.sample_batch.mark_as_processed(
            db=db, db_obj=sample_batch, url=url)
    except SampleBatchAlreadyProccesed:
        raise HTTPException(
            status_code=400, detail="El lote ya fue procesado."
        )
    for sample in sample_batch.samples:
        crud.study.update_state(
            db=db, db_obj=sample.study, new_state=StudyState.STATE_EIGHT,
            employee_id=current_user.id,
            entry_date=sample_batch.current_state_entered_date)
    return sample_batch
