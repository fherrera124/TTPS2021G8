# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User, InformantDoctor, Patient, Employee  # noqa
from app.models.item import Item  # noqa
from app.models.study import Study # noqa
from app.models.health_insurance import HealthInsurance # noqa