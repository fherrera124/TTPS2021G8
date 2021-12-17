import sys
sys.path.append("/")
from app.db.session import SessionLocal
from app import crud, models, schemas
import logging
from time import sleep
from datetime import datetime, timedelta
from app.constants.state import StudyState
from sqlalchemy import and_


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


# Anular estudios que no fueron pagados pasados 30 dias del inicio

filter_before = datetime.today() - timedelta(days=30)
studies = db.query(models.Study).filter(
    and_(models.Study.current_state == StudyState.STATE_ONE,
         models.Study.created_date <= filter_before)).all()


for study in studies:
    crud.study.update_state(db=db, study=study,
                            new_state=StudyState.STATE_ONE_ERROR)


# Cancelar turnos de estudios que pasaron 30 días del turno asignado

studies = db.query(models.Study).join(models.Appointment).filter(
    and_(models.Study.current_state == StudyState.STATE_FOUR,
         models.Appointment.date_appointment <= filter_before)).all()

for study in studies:
    crud.appointment.remove(db=db, id=study.appointment.id)
    crud.study.update_state(db=db, study=study,
                            new_state=StudyState.STATE_THREE)


# Marcar estudios con muestra retrasadas (90 dias)

filter_before = datetime.today() - timedelta(days=90)

studies = db.query(models.Study).join(models.Sample).filter(
    and_(models.Study.current_state == StudyState.STATE_FIVE,
         models.Sample.created_date <= filter_before)).all()

for study in studies:
    crud.study.mark_delayed(db=db, db_obj=study)