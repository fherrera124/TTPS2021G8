from sqlalchemy.orm import Session
from app.models import Appointment, Study
from app.schemas import AppointmentCreate, AppointmentUpdate
from app.crud.base import CRUDBase
from typing import Dict, Union, Any, List, Optional
from app.crud.exceptions import StudyAlreadyWithAppointment, AppointmentOverlap
from app.constants.state import AppointmentState
from datetime import date
from sqlalchemy import func


class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):

    def _check_overlap(self):
        if 2 == 3:  # TODO: implementar
            raise AppointmentOverlap()

    def create(
        self, db: Session, study_id: int, obj_in: Union[AppointmentCreate, Dict[str, Any]]
    ) -> Appointment:
        if 2 == 3:  # TODO: implementar
            raise StudyAlreadyWithAppointment()
        self._check_overlap()
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**create_data, study_id=study_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        self.update_state(
            db=db, appointment=db_obj, new_state=AppointmentState.STATE_PENDING)
        return db_obj

    def get_multi(
            self, db: Session, date: date) -> List[Appointment]:
        return db.query(Appointment).filter(
            func.date(Appointment.date_appointment) == date).all()

    def get_multi(
        self, db: Session,
        skip: int = 0, limit: int = 100,
        state: Optional[str] = None,
        patient_id: Optional[int] = None,
        *,
        date: Optional[date] = None
    ) -> List[Appointment]:
        res = db.query(Appointment)
        if patient_id:
            res = res.join(Study).\
                filter(Study.patient_id == patient_id)
        if state:
            res = res.filter(
                Appointment.current_state == state)
        if date:
            res = res.filter(
                func.date(Appointment.date_appointment) == date)
        return res.offset(skip).limit(limit).all()

    def cancel(self, db: Session, appointment: Appointment) -> Appointment:
        self.update_state(db=db, appointment=appointment,
                          new_state=AppointmentState.STATE_CANCELLED)
        return appointment

    def update_state(self, db: Session, appointment: Appointment, new_state: str) -> Appointment:
        appointment.current_state = new_state
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment


appointment = CRUDAppointment(Appointment)
