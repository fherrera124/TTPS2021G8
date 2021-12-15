from collections import defaultdict
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean, Column, ForeignKey,
    Integer, String, Date, Text, event
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.base_class import Base
from app.constants.role import Role
from sqlalchemy.event import listens_for


if TYPE_CHECKING:
    from .health_insurance import HealthInsurance  # noqa: F401
    from .study import Study  # noqa: F401
    from .study_updates import StudyStates  # noqa: F401


def receive_mapper_configured(mapper, class_):
    mapper.polymorphic_map = defaultdict(
        lambda: mapper, mapper.polymorphic_map)
    # to prevent 'incompatible polymorphic identity' warning, not necessary
    mapper._validate_polymorphic_identity = None


def polymorphic_fallback(mapper_klass):
    event.listens_for(mapper_klass, 'mapper_configured')(
        receive_mapper_configured)
    return mapper_klass


@polymorphic_fallback  # https://stackoverflow.com/a/50983187
class User(Base):
    # NOTA: al aplicarse Single table inheritance,
    # subclases de User no pueden tener NOT NULL constraint.
    # Se los fuerza en los squemas (los llamados "pydantic models")
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }


class Admin(User):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': Role.ADMIN["name"]
    }


class Config(User):
    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': Role.CONFIGURATOR["name"]
    }


class ReportingPhysician(User):
    # (*) en squema.ReportingCreate se asegura
    # el NOT NULL constraint en el campo

    __tablename__ = None

    license = Column(Integer, unique=True, nullable=True)  # *
    reports = relationship(
        "Report", primaryjoin="ReportingPhysician.id == Report.reporting_physician_id", back_populates="reporting_physician")
    __mapper_args__ = {
        'polymorphic_identity': Role.REPORTING_PHYSICIAN["name"]
    }


class Patient(User):
    # (*) en squema.PatientCreate se asegura
    # el NOT NULL constraint en los campos

    __tablename__ = None
    force_password_change = Column(Boolean(), default=True)
    email = Column(String, unique=True, index=True, nullable=True)  # *
    phone_number = Column(String, nullable=True)  # *
    address = Column(String, index=True, nullable=True)  # *
    dni = Column(Integer, unique=True, nullable=True)  # *
    birth_date = Column(Date(), nullable=True)  # *
    first_name_tutor = Column(String, nullable=True)
    last_name_tutor = Column(String, nullable=True)
    health_insurance_number = Column(String)
    health_insurance_id = Column(Integer, ForeignKey("healthinsurance.id"))
    health_insurance = relationship(
        "HealthInsurance", back_populates="affiliates")
    studies = relationship(
        "Study", primaryjoin="Patient.id == Study.patient_id", back_populates="patient")
    clinical_history = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': Role.PATIENT["name"]
    }


class Employee(User):
    __tablename__ = None

    studies_started = relationship(
        "Study", primaryjoin="Employee.id == Study.employee_id", back_populates="patient")

    studies_updated = relationship(
        "StudyStates", primaryjoin="Employee.id == StudyStates.employee_id", back_populates="employee")

    __mapper_args__ = {
        'polymorphic_identity': Role.EMPLOYEE["name"]
    }


@listens_for(Patient, 'after_update')
def after_update_function(mapper, connection, target):
    print("##########################")
    print(target.username)
