from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login, employees, patients,
    studies, health_insurances, utils,
    reporting_physicians, referring_physicians,
    type_studies, presumptive_diagnoses,
    samples, sample_batches, configurators,
    appointments
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])
api_router.include_router(configurators.router, prefix="/configurators", tags=["Configurators"])
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(referring_physicians.router, prefix="/referring-physician", tags=["Referring Physicians"])
api_router.include_router(reporting_physicians.router, prefix="/reporting-physicians", tags=["Reporting Physicians"])
api_router.include_router(studies.router, prefix="/studies", tags=["Studies"])
api_router.include_router(type_studies.router, prefix="/type-studies", tags=["Types of Studies"])
api_router.include_router(presumptive_diagnoses.router, prefix="/presumptive_diagnoses", tags=["Presumptive Diagnoses"])
api_router.include_router(samples.router, prefix="/samples", tags=["Samples"])
api_router.include_router(sample_batches.router, prefix="/sample_batches", tags=["Sample Batches"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(health_insurances.router, prefix="/health_insurances", tags=["Health Insurances"])
