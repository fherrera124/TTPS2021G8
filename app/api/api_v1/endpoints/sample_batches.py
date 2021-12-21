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
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Get batch by ID.
    """
    batch = crud.sample_batch.get(db=db, id=id)
    if not batch:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return batch


@router.post("/{id}/mark-as-processed", response_model=schemas.SampleBatch)
def mark_batch_as_processed(
    id: int,
    url: str,
    rejected_samples: List[int],
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    sample_batch = retrieve_sample_batch(
        db, id, expected_state=SampleBatchState.STATE_ONE)
    # Primero, eliminar las muestras que se rechazan
    # y volver los estudios correspondientes al estado
    # de espera de selección de turno
    for sample_id in rejected_samples:
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
    # Segundo, marcar el lote como procesado. Con
    # las muestras aptas, se pasan los estudios
    # correspondientes al estado de espera de interpretación
    try:
        sample_batch = crud.sample_batch.mark_as_processed(
            db=db, db_obj=sample_batch, url=url)
    except SampleBatchAlreadyProccesed:
        raise HTTPException(
            status_code=400, detail="El lote ya fue procesado."
        )
    for sample in sample_batch.samples:  # en teoria, ya no deberian estar los eliminados
        crud.study.update_state(
            db=db, study=sample.study, new_state=StudyState.STATE_EIGHT,
            updated_by_id=current_user.id,
            entry_date=sample_batch.current_state_entered_date)
    return sample_batch
