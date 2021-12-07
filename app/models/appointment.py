from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_appointment = Column(DateTime, nullable=False)
    description = Column(String)
    study_id = Column(Integer, ForeignKey("study.id"))
    study = relationship(
        "Study", primaryjoin="Appointment.study_id == Study.id",
        back_populates="appointment")
