#Obra social, diagnóstico presuntivo, tipo de estudio y presupuesto.

from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Budget(Base):
    id = Column(Integer, primary_key=True, index=True)
    #health_insurance = 
    presumptive_diagnosis_id = Column(Integer, ForeignKey("diagnosis.id"))
    presumptive_diagnosis = relationship("Diagnosis",
                                         primaryjoin="Study.presumptive_diagnosis_id == Diagnosis.id", back_populates="studies")
    name = Column(String, unique=True, nullable=False)
    studies = relationship(
        "Study", primaryjoin="Diagnosis.id == Study.presumptive_diagnosis_id",
        back_populates="presumptive_diagnosis")
