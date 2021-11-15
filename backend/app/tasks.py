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
    crud.study.update_state(db=db, db_obj=study,
                            new_state=StudyState.STATE_ONE_ERROR)


# TODO: Cancelar turnos de estudios que pasaron 30 días del turno asignado

# Tambien buscar estudios con muestra retrasados (60 dias)