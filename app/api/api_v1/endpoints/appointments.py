from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.crud import StudyAlreadyWithAppointment, AppointmentOverlap
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from datetime import datetime, date, timedelta

router = APIRouter()


def init_list(date: date) -> List[schemas.Appointment]:
    start = datetime(date.year, date.month, date.day, hour=9)
    end = datetime(date.year, date.month, date.day, hour=13)
    delta = timedelta(minutes=15)
    l = []
    while start < end:
        app = schemas.AppointmentSimplified(
            start=start.strftime("%H:%M"), end=(start+delta).strftime("%H:%M"))
        l.append(app)
        start = start+delta
    return l


@ router.post("/", response_model=List[schemas.AppointmentSimplified])
def appointments(
    date: date = Body(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
) -> Any:
    """
    Retrieve appointments of a given date.
    """
    if date.weekday() in (5, 6): # sabado o domingo
        return []
    appointments = crud.appointment.get_multi(db=db, date=date)

    schedule_list = init_list(date=date)

    for appointment in appointments:
        start = appointment.date_appointment.strftime("%H:%M")
        for schedule in schedule_list:
            if schedule.start == start:
                patient = appointment.study.patient
                schedule.patient = {"first_name": patient.first_name,
                                "last_name": patient.last_name}
                break
        else:
            continue  # only executed if the inner loop did NOT break
        break  # only executed if the inner loop DID break
    return schedule_list

#TODO: un endpoint que sea turnos cancelados