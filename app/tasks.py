from sqlalchemy import and_
from app.constants.state import StudyState, AppointmentState
from datetime import datetime, timedelta
from time import sleep
import logging
from app import crud, models, schemas
from app.db.session import SessionLocal
import sys
sys.path.append("/")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('-- Tareas diarias --')

try:
    db = SessionLocal()
    # Try to create session to check if DB is awake
    db.execute("SELECT 1")
except Exception as e:
    logger.error(e)
    raise e


res = db.query(models.Study)

# Anular estudios que no fueron pagados pasados 30 dias del inicio

filter_before = datetime.today() - timedelta(days=30)
studies = res.filter(
    models.Study.current_state == StudyState.STATE_ONE,
    models.Study.created_date <= filter_before).all()
for study in studies:
    crud.study.update_state(db=db, study=study,
                            new_state=StudyState.STATE_ONE_ERROR)


# Marcar estudios con muestra retrasadas (90 dias)

filter_before = datetime.today() - timedelta(days=90)
studies = res.join(models.Sample).filter(
    models.Study.current_state == StudyState.STATE_FIVE,
    models.Sample.created_date <= filter_before).all()
for study in studies:
    crud.study.mark_delayed(db=db, db_obj=study)


# Cancelar turnos de estudios que pasaron 30 días del turno asignado

appointments = db.query(models.Appointment).filter(
    models.Appointment.current_state == AppointmentState.STATE_PENDING,
    models.Appointment.date_appointment <= filter_before).all()
for appointment in appointments:
    crud.appointment.cancel(db=db, appointment=appointment)
    crud.study.update_state(db=db, study=appointment.study,
                            new_state=StudyState.STATE_THREE)
