from sqlalchemy.orm import Session
from app.models import HealthInsurance
from app.schemas import HealthInsuranceCreate, HealthInsuranceUpdate
from app.crud.base import CRUDBase

class CRUDHealthInsurance(CRUDBase[HealthInsurance, HealthInsuranceCreate, HealthInsuranceUpdate]):
    pass

health_insurance = CRUDHealthInsurance(HealthInsurance)