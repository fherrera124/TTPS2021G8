

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models import ReportingPhysician
from sqlalchemy.ext.hybrid import hybrid_property
from app.constants.state import StudyState, StudyStatePatientView


class StudyStates(Base):
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("study.id"))
    study = relationship(
        "Study", primaryjoin="StudyStates.study_id == Study.id",
        back_populates="states")
    state = Column(String)
    state_entered_date = Column(DateTime(timezone=True))
    updated_by_id = Column(Integer, ForeignKey('user.id'))
    updated_by = relationship(
        "User", primaryjoin="StudyStates.updated_by_id == User.id", back_populates="studies_updated")

    @hybrid_property
    def state_patient_view(self):
        # Esta propiedad hibrida me permite definir
        # un atributo que se construye "on the fly"
        # a nivel de Python, siendo trasparente a la db.
        state_translation = {
            StudyState.STATE_ONE: StudyStatePatientView.STATE_ONE,
            StudyState.STATE_ONE_ERROR: StudyStatePatientView.STATE_ONE_ERROR,
            StudyState.STATE_TWO: StudyStatePatientView.STATE_TWO,
            StudyState.STATE_THREE: StudyStatePatientView.STATE_THREE,
            StudyState.STATE_FOUR: StudyStatePatientView.STATE_FOUR,
            StudyState.STATE_FIVE: StudyStatePatientView.STATE_FIVE,
            StudyState.STATE_SIX: StudyStatePatientView.STATE_SIX,
            StudyState.STATE_SEVEN: StudyStatePatientView.STATE_SIX,
            StudyState.STATE_EIGHT: StudyStatePatientView.STATE_SIX,
            StudyState.STATE_NINE: StudyStatePatientView.STATE_SIX,
            StudyState.STATE_ENDED: StudyStatePatientView.STATE_ENDED,
        }
        return state_translation[self.state]

    @hybrid_property
    def state_entered_date_patient_view(self):
        # Como los estados 7, 8, 9 son transparentes al paciente,
        # además de sólo mostrar el estado 6, debemos asegurarnos
        # de mostrar la fecha de dicho estado.
        if self.state in (
            StudyState.STATE_SEVEN,
            StudyState.STATE_EIGHT,
            StudyState.STATE_NINE
        ): # FIXME
            #state_six = db.query(StudyStates).filter(
            #    StudyStates.study_id == self.study_id,
            #    StudyStates.state == StudyState.STATE_SIX)
            #return state_six.state_entered_date
            return self.state_entered_date
        else:
            return self.state_entered_date


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
