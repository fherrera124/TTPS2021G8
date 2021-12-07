# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
<<<<<<< HEAD
from app.models.user import User, ReportingPhysician, Patient, Employee  # noqa
from app.models.study import Study, TypeStudy # noqa
from app.models.study_updates import StudyStates, Report # noqa
from app.models.diagnosis import Diagnosis # noqa
from app.models.health_insurance import HealthInsurance # noqa
from app.models.referring_physician import ReferringPhysician  # noqa
from app.models.sample import Sample # noqa
from app.models.sample_batch import SampleBatch # noqa
from app.models.appointment import Appointment # noqa
=======
from app.models.user import User, InformantDoctor, Patient, Employee  # noqa
from app.models.item import Item  # noqa
from app.models.study import Study # noqa
from app.models.health_insurance import HealthInsurance # noqa
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
