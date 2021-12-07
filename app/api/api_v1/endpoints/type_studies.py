from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Security, Body
from sqlalchemy.orm import Session
from weasyprint import HTML, CSS
from fastapi.responses import Response
from app import crud, schemas, models
from app.api import deps
from weasyprint.text.fonts import FontConfiguration
from app.constants.css import CSS as Css
from app.constants.role import Role


router = APIRouter()


@router.get("/", response_model=List[schemas.TypeStudy])
def read_study_types(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.CONFIGURATOR["name"]]
        )
) -> Any:
    """
    Retrieve study types.
    """
    study_types = crud.type_study.get_multi(db, skip=skip, limit=limit)
    return study_types


@router.post("/", response_model=schemas.TypeStudy)
def create_type_study(
        type_study_in: schemas.TypeStudyCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.CONFIGURATOR["name"]]
        )
) -> Any:
    """
    Create new type study.
    """
    type_study = crud.type_study.get_by_name(db, name=type_study_in.name)
    if type_study:
        raise HTTPException(
            status_code=400,
            detail="The type study with this name already exists in the system.",
        )
    type_study = crud.type_study.create(db, obj_in=type_study_in)
    print('CREADO', type_study)
    return type_study


@router.get("/{type_study_id}", response_model=schemas.TypeStudy)
def read_type_study_by_id(
        type_study_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a type study by id.
    """
    type_study = crud.type_study.get(db, id=type_study_id)
    if not type_study:
        raise HTTPException(
            status_code=400,
            detail="No existe en el sistema el tipo de estudio con la id ingresada.",
        )
    return type_study


@router.put("/{type_study_id}", response_model=schemas.TypeStudy)
def update_type_study_template(
        type_study_id: int,
        template: str = Body(...),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.CONFIGURATOR["name"]]
        )
) -> Any:
    """
    Update a type study template.
    """
    type_study = crud.type_study.get(db, id=type_study_id)
    if not type_study:
        raise HTTPException(
            status_code=404,
            detail="No existe en el sistema el tipo de estudio con la id ingresada.",
        )
    type_study = crud.type_study.update_template(
        db=db, db_obj=type_study, template=template)
    return type_study


@router.get("/get-study-consent-template/{type_study_id}")
def generate_pdf(
        type_study_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
      Return a pdf with consent template text.
    """
    font_config = FontConfiguration()
    type_study = crud.type_study.get(db, id=type_study_id)
    html = HTML(string=type_study.study_consent_template,
                encoding='UTF-8')
    css = CSS(string=Css.CSS, font_config=font_config)

    return Response(content=html.write_pdf(stylesheets=[css],
                                           font_config=font_config), media_type="application/pdf")
