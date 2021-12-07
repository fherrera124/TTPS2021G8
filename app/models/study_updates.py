

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models import Employee, ReportingPhysician


class StudyStates(Base):
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("study.id"))
    study = relationship(
        "Study", primaryjoin="StudyStates.study_id == Study.id",
        back_populates="states")
    state = Column(String)
    state_entered_date = Column(DateTime(timezone=True))
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship(
        "Employee", primaryjoin="StudyStates.employee_id == Employee.id", back_populates="studies_updated")


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("study.id"))
    study = relationship(
        "Study", primaryjoin="Report.study_id == Study.id", back_populates="report")

    reporting_physician_id = Column(Integer, ForeignKey(ReportingPhysician.id))
    reporting_physician = relationship(
        "ReportingPhysician", primaryjoin="Report.reporting_physician_id == ReportingPhysician.id", back_populates="reports")

    result = Column(String, default=False)
    date_report = Column(DateTime, server_default=func.now())
    report = Column(Text)
