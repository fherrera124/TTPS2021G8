from .crud_user import admin, config, user, employee, patient, reporting_physician
from .crud_study import study
from .crud_study_states import study_states
from .crud_report import report
from .crud_referring_physician import referring_physician
from .crud_type_study import type_study
from .crud_sample import sample
from .crud_sample_batch import sample_batch
from .crud_appointment import appointment
from .crud_health_insurance import health_insurance
from .exceptions import *


# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)