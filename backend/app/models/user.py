from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean, Column, ForeignKey,
    Integer, String, Date, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .health_insurance import HealthInsurance  # noqa: F401
    from .study import Study # noqa: F401
    from .item import Item # noqa: F401


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    type = Column(String(20))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }


class InformantDoctor(User):
    __tablename__=None
    
    licence = Column(Integer, nullable=False)
    studies_informed = relationship("Study", back_populates="informant_doctor")
    __mapper_args__ = {
        'polymorphic_identity': 'informantdoctor'
    }


class Patient(User):
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
    }


class Employee(User):
    __tablename__=None
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }
