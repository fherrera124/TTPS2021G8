from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Diagnosis(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    studies = relationship(
        "Study", primaryjoin="Diagnosis.id == Study.presumptive_diagnosis_id",
        back_populates="presumptive_diagnosis")
