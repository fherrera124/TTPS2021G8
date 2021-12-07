from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import Patient  # noqa: F401


class HealthInsurance(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    telephone = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    affiliates = relationship("Patient", back_populates="health_insurance")
