from app.models import SampleBatch
from app.schemas import SampleBatchCreate, SampleBatchUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
from app.constants.state import SampleBatchState
from app.crud.exceptions import SampleBatchAlreadyProccesed

class CRUDSampleBatch(CRUDBase[SampleBatch, SampleBatchCreate, SampleBatchUpdate]):
    def mark_as_processed(
            self, db: Session, db_obj: SampleBatch, url: str) -> Optional[SampleBatch]:
        if db_obj.current_state == SampleBatchState.STATE_TWO:
            raise SampleBatchAlreadyProccesed
        db_obj.current_state = SampleBatchState.STATE_TWO
        db_obj.url = url
        db_obj.current_state_entered_date = func.now()
        db.commit()
        db.refresh(db_obj)
        return db_obj


sample_batch = CRUDSampleBatch(SampleBatch)
