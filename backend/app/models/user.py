from collections import defaultdict
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean, Column, ForeignKey,
<<<<<<< HEAD
    Integer, String, Date, Text, event
=======
    Integer, String, Date, Text
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

from app.db.base_class import Base
from app.constants.role import Role
from sqlalchemy.event import listens_for


if TYPE_CHECKING:
    from .health_insurance import HealthInsurance  # noqa: F401
<<<<<<< HEAD
    from .study import Study  # noqa: F401
    from .study_updates import StudyStates  # noqa: F401


def receive_mapper_configured(mapper, class_):
    mapper.polymorphic_map = defaultdict(
        lambda: mapper, mapper.polymorphic_map)
    # to prevent 'incompatible polymorphic identity' warning, not necessary
    mapper._validate_polymorphic_identity = None

=======
    from .study import Study # noqa: F401
    from .item import Item # noqa: F401
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3

def polymorphic_fallback(mapper_klass):
    event.listens_for(mapper_klass, 'mapper_configured')(
        receive_mapper_configured)
    return mapper_klass


@polymorphic_fallback  # https://stackoverflow.com/a/50983187
class User(Base):
<<<<<<< HEAD
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
=======
    email = Column(String, unique=True, index=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    type = Column(String(20))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }


<<<<<<< HEAD
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
=======
class InformantDoctor(User):
    __tablename__=None
    
    licence = Column(Integer, nullable=False)
    studies_informed = relationship("Study", back_populates="informant_doctor")
    __mapper_args__ = {
        'polymorphic_identity': 'informantdoctor'
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
    }


class Patient(User):
<<<<<<< HEAD
    # (*) en squema.PatientCreate se asegura
    # el NOT NULL constraint en los campos

    __tablename__ = None
    email = Column(String, unique=True, index=True, nullable=True)  # *
    dni = Column(Integer, unique=True, nullable=True)  # *
    birth_date = Column(Date(), nullable=True)  # *
    health_insurance_number = Column(String)
    health_insurance_id = Column(Integer, ForeignKey("healthinsurance.id"))
    health_insurance = relationship(
        "HealthInsurance", back_populates="affiliates")
    studies = relationship(
        "Study", primaryjoin="Patient.id == Study.patient_id", back_populates="patient")
    clinical_history = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': Role.PATIENT["name"]
=======
    __tablename__=None
    
    dni = Column(Integer, nullable=False)
    birth_date = Column(Date(), nullable=False)
    health_insurance_number = Column(Integer)
    health_insurance_id= Column(Integer, ForeignKey("healthinsurance.id"))
    health_insurance = relationship(
        "HealthInsurance", back_populates="affiliates")
    studies = relationship("Study", back_populates="patient")
    clinical_history = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
    }


class Employee(User):
<<<<<<< HEAD
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
=======
    __tablename__=None
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }
>>>>>>> f6df114451f33d105fe9eb5fae6d04d25901e3c3
