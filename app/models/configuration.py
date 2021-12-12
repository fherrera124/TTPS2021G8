from sqlalchemy import Column, Integer, DateTime, Boolean
from app.db.base_class import Base
from sqlalchemy.sql import func

class Configuration(Base):
    id = Column(Integer, primary_key=True, index=True)
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())
    obligated_mode = Column(Boolean, default=False)
