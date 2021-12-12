from sqlalchemy.orm import Session
from app.models import Configuration
from app.schemas import ConfigurationCreate, ConfigurationUpdate
from app.crud.base import CRUDBase
from typing import Optional


class CRUDConfiguration(CRUDBase[Configuration, ConfigurationCreate, ConfigurationUpdate]):
    def get_config(self, db: Session) -> Optional[Configuration]:
        return db.query(self.model).first()

config = CRUDConfiguration(Configuration)