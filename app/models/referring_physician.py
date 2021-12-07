from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class ReferringPhysician(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license = Column(Integer, unique=True, index=True, nullable=False)
    phone = Column(String)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    studies_referred = relationship(
        "Study", primaryjoin="ReferringPhysician.id == Study.referring_physician_id",
        back_populates="referring_physician")
