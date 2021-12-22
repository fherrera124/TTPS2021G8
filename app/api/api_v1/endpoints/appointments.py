from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.crud import StudyAlreadyWithAppointment, AppointmentOverlap
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.constants.state import AppointmentState
from datetime import datetime, date, timedelta

router = APIRouter()


def _retrieve_appointment(
    db: Session,
    id: int,
    expected_state: Optional[str] = None
) -> Optional[models.Appointment]:
    appointment = crud.appointment.get(db=db, id=id)
    if appointment is None:
        raise HTTPException(
            status_code=404, detail="No se encontró el turno"
        )
    if expected_state is None or expected_state == appointment.current_state:
        return appointment
    raise HTTPException(
        status_code=400, detail="Acción incompatible con el estado del turno"
    )


@router.get("/", response_model=List[schemas.Appointment])
def read_appointments(
    date: Optional[date] = None,
    state: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"],
                Role.PATIENT["name"]],
    )
) -> Any:
    """
    Retrieve appointments.
    Date is optional.
    Example of date: 2021-12-21
    """
    if crud.user.is_patient(current_user):
        appointments = crud.appointment.get_multi(
            db, skip=skip, limit=limit,
            patient_id=current_user.id,
            date=date, state=state
        )
    else:  # employee
        appointments = crud.appointment.get_multi(
            db, skip=skip, limit=limit,
            date=date, state=state
        )
    return appointments


@router.get("/{id}", response_model=schemas.Appointment)
def read_appointment(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.PATIENT["name"]]
    )
) -> Any:
    """
    Get appointment by ID.
    """
    appointment = _retrieve_appointment(db=db, id=id)
    if crud.user.is_patient(current_user):
        if current_user.id != appointment.study.patient_id:
            raise HTTPException(
                status_code=400,
                detail="El turno no corresponde al paciente"
            )
    return appointment


@router.post("/{id}/cancel", response_model=schemas.Appointment)
def cancel_appointment(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.PATIENT["name"]],
    ),
) -> Any:
    """
    Cancel an appointment.
    """
    appointment = _retrieve_appointment(
        db=db, id=id, expected_state=AppointmentState.STATE_PENDING)
    if crud.user.is_patient(current_user):
        if current_user.id != appointment.study.patient_id:
            raise HTTPException(
                status_code=400,
                detail="El turno no corresponde al paciente"
            )
    crud.appointment.cancel(db=db, appointment=appointment)
    return appointment


def _init_list(date: date) -> List[schemas.AppointmentSimplified]:
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


@router.post("/", response_model=List[schemas.AppointmentSimplified])
def simplified_appointments(
    date_appointment: date = Body(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    ),
) -> Any:
    """
    Retrieve a simplified list of appointments of a given date.
    """
    if date_appointment.weekday() in (5, 6):  # sabado o domingo
        return []
    if date_appointment < date.today():  # dias anteriores a hoy
        return []
    appointments = crud.appointment.get_multi(db=db, date=date_appointment)
    schedule_list = _init_list(date=date_appointment)
    for appointment in appointments:
        start = appointment.date_appointment.strftime("%H:%M")
        for schedule in schedule_list:
            if schedule.start == start:
                patient = appointment.study.patient
                schedule.patient = {
                    "first_name": patient.first_name,
                    "last_name": patient.last_name
                }
                break
    return schedule_list
