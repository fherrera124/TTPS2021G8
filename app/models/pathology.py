from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Pathology(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
