from sqlalchemy.orm import Session
from app.models import Appointment, Study
from app.schemas import AppointmentCreate, AppointmentUpdate
from app.crud.base import CRUDBase
from typing import Dict, Union, Any, List
from app.crud.exceptions import StudyAlreadyWithAppointment, AppointmentOverlap
from datetime import date
from sqlalchemy import func

class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):

    def _check_overlap(self):
        if False:  # TODO: implementar
            raise AppointmentOverlap()

    def create(
        self, db: Session, study_id: int, obj_in: Union[AppointmentCreate, Dict[str, Any]]
    ) -> Appointment:

        if False:  # TODO: implementar
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
        return db_obj

    def get_multi(
            self, db: Session, date: date) -> List[Appointment]:
        return db.query(Appointment).filter(
            func.date(Appointment.date_appointment) == date).all()


appointment = CRUDAppointment(Appointment)
