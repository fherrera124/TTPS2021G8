from typing import Any, List, Optional
from fastapi import (
    APIRouter, Depends, HTTPException,
    Security, File, UploadFile, Body
)
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.constants.state import StudyState
from app.crud.exceptions import *
from app.core.mail import conf
from weasyprint import HTML
from fastapi.responses import Response
from fastapi_mail import FastMail, MessageSchema
from io import BytesIO

router = APIRouter()


@router.get("/", response_model=List[schemas.Study])
def read_studies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"], Role.REPORTING_PHYSICIAN["name"]],
    )
) -> Any:
    """
    Retrieve studies.
    """
    if crud.user.is_reporting_physician(current_user):
        studies = crud.study.get_multi(
            db, skip=skip, limit=limit, state=StudyState.STATE_EIGHT)
    else:
        studies = crud.study.get_multi(db, skip=skip, limit=limit)
    return studies


@router.get("/delayed", response_model=List[schemas.Study])
def read_delayed_studies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Retrieve delayed studies.
    """
    studies = crud.study.get_multi_delayed(db, skip=skip, limit=limit)
    return studies


@router.post("/", response_model=schemas.Study)
async def create_study(
    *,
    db: Session = Depends(deps.get_db),
    study_in: schemas.StudyCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]],
    )
) -> Any:
    """
    Create new study.
    """
    study = crud.study.create(
        db=db, obj_in=study_in, employee_id=current_user.id)
    email = study.patient.email
    pdf = generate_budget_pdf(study=study)
    file = UploadFile(filename="presupuesto.pdf", file=BytesIO(pdf))
    message = MessageSchema(
        subject="mylab",
        recipients=[email],
        body="Hola, le adjunto el presupuesto del estudio de laboratorio.",
        attachments=[file]
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return study


def generate_budget_pdf(study: models.Study) -> bytes:
    patient = study.patient
    ref_physician = study.referring_physician
    with open('/app/templates/budget.html', 'r') as file:
        file_budget = file.read().replace('\n', '')
    replacements = {
        'created_date': study.created_date.strftime("%m/%d/%Y"), 'patient_first_name': patient.first_name,
        'patient_last_name': patient.last_name, 'patient_dni': patient.dni,
        'physician_first_name': ref_physician.first_name, 'physician_last_name': ref_physician.last_name,
        'physician_license': ref_physician.license, 'type_study': study.type_study.name,
        'presumptive_diagnosis': study.presumptive_diagnosis.name, 'budget': study.budget,
    }
    body = file_budget.format(**replacements)
    pdf = HTML(string=body, encoding='UTF-8').write_pdf()
    return pdf


@router.get("/{id}/download-budget", response_class=Response)
def download_budget(
    id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id)
    pdf = generate_budget_pdf(study=study)
    return Response(content=pdf, media_type="application/pdf")


@router.get("/{id}/download-consent", response_class=Response)
def download_consent(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id)
    type_study = crud.type_study.get(db, id=study.type_study_id)
    pdf = HTML(string=type_study.study_consent_template,
               encoding='UTF-8').write_pdf()
    return Response(content=pdf, media_type="application/pdf")


@router.put("/{id}", response_model=schemas.Study)
def update_study(
    id: int,
    study_in: schemas.StudyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    )
) -> Any:
    """
    Update a study.
    """
    study = crud.study.get(db=db, id=id)
    if not study:
        raise HTTPException(
            status_code=404, detail="No se encontró el estudio.")
    if not crud.user.is_admin(current_user) and (study.employee_id != current_user.id):
        raise HTTPException(
            status_code=400, detail="No tiene permisos para la acción solicitada.")
    study = crud.study.update(db=db, db_obj=study, obj_in=study_in)
    return study


@router.get("/{id}", response_model=schemas.Study)
def read_study(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    )
) -> Any:
    """
    Get study by ID.
    """
    # TODO: permitir acceder a medico informante, pero asegurarse que el estudio
    # estén en estado "Esperando interpretación de resultados e informes"
    study = crud.study.get(db=db, id=id)
    if not study:
        raise HTTPException(
            status_code=404, detail="No se encontró el estudio.")
    return study


def retrieve_study(db: Session, id: int, expected_state: Optional[str] = None) -> Optional[models.Study]:
    study = crud.study.get(db=db, id=id)
    if study is None:
        raise HTTPException(
            status_code=404, detail="No se encontró el estudio"
        )
    if expected_state is None or expected_state == study.current_state:
        return study
    raise HTTPException(
        status_code=400, detail="Acción incompatible con el estado del estudio"
    )


@router.post("/{id}/payment-receipt/")
async def payment_receipt(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_ONE)
    study.payment_receipt = file.filename
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_TWO, employee_id=current_user.id)
    return {"filename": file.filename}


# @router.get("/{id}/payment-receipt/")
# def payment_receipt(
#     id: int,
#     # current_user: models.User = Security(
#     #     deps.get_current_active_user,
#     #     scopes=[Role.EMPLOYEE["name"]]
#     # ),
#     db: Session = Depends(deps.get_db)
# ) -> Any:
#     study = retrieve_study(db, id)
#     if study.payment_receipt is None:
#         raise HTTPException(
#             status_code=404, detail="No hay registro de comprobante de pago para el estudio"
#         )
#     return {"filename": study.payment_receipt}


@router.get("/{id}/download-consent", response_class=Response)
def download_consent(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id)
    type_study = crud.type_study.get(db, id=study.type_study_id)
    pdf = HTML(string=type_study.study_consent_template,
               encoding='UTF-8').write_pdf()
    return Response(content=pdf, media_type="application/pdf")


@router.post("/{id}/signed-consent")
async def signed_consent(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_TWO)
    study.signed_consent = file.filename
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_THREE, employee_id=current_user.id)
    return {"filename": file.filename}


@router.post("/{id}/register-appointment", response_model=schemas.Appointment)
def register_appointment(
    id: int,
    appointment_in: schemas.AppointmentCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_THREE)
    try:
        appointment = crud.appointment.create(
            db=db, study_id=study.id, obj_in=appointment_in)
    except StudyAlreadyWithAppointment:
        raise HTTPException(
            status_code=400,
            detail="El estudio ya registra un turno",
        )
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_FOUR, employee_id=current_user.id)
    return appointment


@router.post("/{id}/register-sample", response_model=schemas.Sample)
def register_sample(
    id: int,
    sample_in: schemas.SampleCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_FOUR)
    try:
        sample = crud.sample.create(db=db, study_id=id, obj_in=sample_in)
    except StudyAlreadyWithSample:
        raise HTTPException(
            status_code=400,
            detail="El estudio ya registra una muestra"
        )
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_FIVE, employee_id=current_user.id)
    return sample


# @router.post("/{id}/test-batch-generation", response_model=schemas.Sample)
# def test-batch-generation(
#     id: int,
#     sample_in: schemas.SampleCreate,
#     current_user: models.User = Security(
#         deps.get_current_active_user,
#         scopes=[Role.EMPLOYEE["name"]]
#     ),
#     db: Session = Depends(deps.get_db)
# ) -> Any:
#     study = retrieve_study(db, id, expected_state=None)
#     try:
#         sample = crud.sample.create(db=db, study_id=id, obj_in=sample_in)
#     except StudyAlreadyWithSample:
#         raise HTTPException(
#             status_code=400,
#             detail="El estudio ya registra una muestra"
#         )
#     crud.study.update_state(
#         db=db, db_obj=study, new_state=StudyState.STATE_SIX, employee_id=current_user.id)
#     return sample


@router.post("/{id}/register-sample-pickup")
def register_sample_pickup(
    id: int,
    picked_up_by: str = Body(...),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_FIVE)
    try:
        sample = crud.sample.register_extractionist(
            db=db, db_obj=study.sample, picked_up_by=picked_up_by)
    except SampleAlreadyPickedUp:
        raise HTTPException(
            status_code=400, detail="La muestra ya fue recogida.")
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_SIX,
        employee_id=current_user.id, entry_date=sample.picked_up_date)
    # no informa si se creó un lote
    return {"El retiro de la muestra fue registrado"}


@router.post("/{id}/add-report", response_model=schemas.Report)
def add_report(
    id: int,
    report_in: schemas.ReportCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.REPORTING_PHYSICIAN["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_EIGHT)
    report = crud.report.create(db=db, study_id=study.id, obj_in=report_in)
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_NINE,
        employee_id=current_user.id, entry_date=report.date_report)
    return report


@router.post("/{id}/send-report")
async def send_report(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id, expected_state=StudyState.STATE_NINE)
    patient = study.patient
    email = study.referring_physician.email
    report = study.report
    rep_physician = report.reporting_physician
    with open('/app/templates/report.html', 'r') as file:
        file_report = file.read().replace('\n', '')
    replacements = {
        'date_report': report.date_report.strftime("%m/%d/%Y"), 'patient_first_name': patient.first_name,
        'patient_last_name': patient.last_name, 'patient_dni': patient.dni,
        'physician_first_name': rep_physician.first_name, 'physician_last_name': rep_physician.last_name,
        'physician_license': rep_physician.license, 'report': report.report, 'result': report.result,
    }
    body = file_report.format(**replacements)
    pdf = HTML(string=body, encoding='UTF-8').write_pdf()
    file = UploadFile(filename="informe.pdf", file=BytesIO(pdf))
    message = MessageSchema(
        subject="mylab",
        recipients=[email],
        body="Hola colega, le adjunto el informe de uno de sus pacientes.",
        attachments=[file]
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    crud.study.update_state(
        db=db, db_obj=study, new_state=StudyState.STATE_ENDED,
        employee_id=current_user.id)
    return {"El reporte fue enviado exitosamente."}


@router.get("/{id}/download-consent", response_class=Response)
def download_consent(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id)
    # TODO: en base al tipo de estudio, devolver el consentimiento
    pdf = HTML(string='<h3>Consentimiento para estudio X</h3><p>En caracter de ...</p>',
               encoding='UTF-8').write_pdf()
    return Response(content=pdf, media_type="application/pdf")


@router.get("/{id}/study-history", response_model=List[schemas.StudyState])
def study_history(
    id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.EMPLOYEE["name"]]
    ),
    db: Session = Depends(deps.get_db)
) -> Any:
    study = retrieve_study(db, id)
    study_states = crud.study_states.get_multi_by_study(
        db=db, study_id=study.id)
    return study_states


# @router.delete("/{id}", response_model=schemas.Study)
# def delete_study(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an study.
#     """
#     study = crud.study.get(db=db, id=id)
#     if not study:
#         raise HTTPException(status_code=404, detail="No se encontró el estudio.")
#     study = crud.study.remove(db=db, id=id)
#     return study
