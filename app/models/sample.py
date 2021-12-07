from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Sample(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    study_id = Column(Integer, ForeignKey('study.id'))
    study = relationship(
        "Study", primaryjoin="Sample.study_id == Study.id",
        back_populates="sample")
    ml_extracted = Column(Float)
    freezer_number = Column(Integer)
    picked_up_by = Column(String, default=None)
    picked_up_date = Column(DateTime(timezone=True))
    sample_batch_id = Column(Integer, ForeignKey('samplebatch.id'))
    sample_batch = relationship("SampleBatch")
    paid = Column(Boolean, default=False)