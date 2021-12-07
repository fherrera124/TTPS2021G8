from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, Text, Date

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base

from .user import InformantDoctor, Patient

class Study(Base):
    id = Column(Integer, primary_key=True, index=True)
    result = Column(Boolean(), default=True) #dudaa, capaz string
    date_report = Column(Date())
    informant_doctor_id = Column(Integer, ForeignKey(InformantDoctor.id))
    informant_doctor = relationship(InformantDoctor, back_populates="studies_informed")
    patient_id = Column(Integer, ForeignKey(Patient.id))
    patient = relationship(Patient, back_populates="studies")
    report = Column(Text)
    status = Column(String(20))