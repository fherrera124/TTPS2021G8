from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.core.config import settings
from app.db import base  # noqa: F401
from app.core.security import get_password_hash

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    admin = crud.admin.get_by_username(db, username=settings.ADMIN_USERNAME)
    if not admin:
        admin_in = schemas.AdminCreate(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            first_name='admin',
            last_name='admin'
        )
        admin = crud.admin.create(db, obj_in=admin_in)  # noqa: F841

    ######### Cargar data inicial ###########


    # Health insurance
    insu1 = models.HealthInsurance(
        name="Osde", telephone="02214662322", email="osdelp@osde.com.ar")
    db.add(insu1)
    insu2 = models.HealthInsurance(
        name="IOMA", telephone="02214663325", email="ioma@gob.ar")
    db.add(insu2)
    db.commit()
    db.refresh(insu1)
    db.refresh(insu2)


    # configuracion

    config = models.Configuration()
    db.add(config)
    db.commit()


    # usuarios del sistema

    users = [

        models.Config(username="configurador",
                      first_name="configurador", last_name="configurador",
                      hashed_password=get_password_hash("changeme")),
        models.ReportingPhysician(
            username="informante", first_name="informante", last_name="informante", license=1288902,
            hashed_password=get_password_hash("changeme")),
        models.ReferringPhysician(first_name="derivante", last_name="derivante",
                                  license=12884629, phone="334892", email="fran.herrera124@gmail.com"),
        models.Patient(username="paciente", dni=26053114, email="fran.herrera124@gmail.com.ar",
                       birth_date="02-01-1975", health_insurance_id=insu1.id, first_name="Juan",
                       last_name="Perez", hashed_password=get_password_hash("changeme")),
        models.Patient(username="carlaconte", dni=26053117, email="carlaconte@gmail.com.ar",
                       birth_date="02-01-1975", health_insurance_id=insu1.id, first_name="Carla",
                       last_name="Conte", hashed_password=get_password_hash("changeme")),
        models.Patient(username="conemail", dni=26053115, email="mjdelafuente@gmail.com",
                       birth_date="02-01-1975", health_insurance_id=insu1.id, first_name="Mario",
                       last_name="Azul", hashed_password=get_password_hash("changeme")),
        models.Patient(username="salfuen", dni=26053111, email="salfuen@gmail.com.ar",
                       birth_date="02-01-1975", health_insurance_id=insu1.id, first_name="Silvia",
                       last_name="Perez", hashed_password=get_password_hash("changeme")),
        models.Employee(username="empleado", first_name="Miguel", last_name="de la Fuente",
                        hashed_password=get_password_hash("changeme"))
    ]

    db.bulk_save_objects(users)

    # Diagnósticos presuntivos

    diagnosis = [
        models.Diagnosis(name="Acidez de estómago"),
        models.Diagnosis(name="Acné"),
        models.Diagnosis(name="Acúfenos"),
        models.Diagnosis(name="Adenoma hipofisiario"),
        models.Diagnosis(name="Aerofagia"),
        models.Diagnosis(name="Aftas bucales"),
        models.Diagnosis(name="Agorafobia"),
        models.Diagnosis(name="Alergia"),
        models.Diagnosis(name="Alergia al látex"),
        models.Diagnosis(name="Alergia al polen"),
        models.Diagnosis(name="Alergias alimentarias"),
        models.Diagnosis(name="Alopecia"),
        models.Diagnosis(name="Alzheimer"),
        models.Diagnosis(name="Amenorrea"),
        models.Diagnosis(name="Amigdalitis"),
        models.Diagnosis(name="Anemia"),
        models.Diagnosis(name="Aneurisma de aorta"),
        models.Diagnosis(name="Angina de pecho"),
        models.Diagnosis(name="Anisakiasis"),
        models.Diagnosis(name="Anorexia"),
        models.Diagnosis(name="Ansiedad"),
        models.Diagnosis(name="Apendicitis"),
        models.Diagnosis(name="Apnea del sueño"),
        models.Diagnosis(name="Arritmias"),
        models.Diagnosis(name="Arterioesclerosis"),
        models.Diagnosis(name="Artritis reumatoide"),
        models.Diagnosis(name="Artrosis"),
        models.Diagnosis(name="Asbestosis"),
        models.Diagnosis(name="Asma"),
        models.Diagnosis(name="Astigmatismo"),
        models.Diagnosis(name="Ataxia"),
        models.Diagnosis(name="Ateroesclerosis"),
        models.Diagnosis(name="Autismo"),
        models.Diagnosis(name="Balanitis"),
        models.Diagnosis(name="Bartolinitis"),
        models.Diagnosis(name="Botulismo"),
        models.Diagnosis(name="Bradicardia"),
        models.Diagnosis(name="Bronquiectasias"),
        models.Diagnosis(name="Bronquitis"),
        models.Diagnosis(name="Brucelosis"),
        models.Diagnosis(name="Bruxismo"),
        models.Diagnosis(name="Bulimia"),
        models.Diagnosis(name="Bullying"),
        models.Diagnosis(name="Bursitis"),
        models.Diagnosis(name="Callos"),
        models.Diagnosis(name="Cáncer de cabeza y cuello"),
        models.Diagnosis(name="Cáncer de colon"),
        models.Diagnosis(name="Cáncer de cuello de útero"),
        models.Diagnosis(name="Cáncer de endometrio"),
        models.Diagnosis(name="Cáncer de estómago"),
        models.Diagnosis(name="Cáncer de faringe"),
        models.Diagnosis(name="Cáncer de intestino delgado"),
        models.Diagnosis(name="Cáncer de laringe"),
        models.Diagnosis(name="Cáncer de las vías biliares"),
        models.Diagnosis(name="Cáncer de mama"),
        models.Diagnosis(name="Cáncer de ovario"),
        models.Diagnosis(name="Cáncer de páncreas"),
        models.Diagnosis(name="Cáncer de piel"),
        models.Diagnosis(name="Cáncer de próstata"),
        models.Diagnosis(name="Cáncer de pulmón"),
        models.Diagnosis(name="Cáncer de riñón"),
        models.Diagnosis(name="Cáncer de testículo"),
        models.Diagnosis(name="Cáncer de tiroides"),
        models.Diagnosis(name="Cáncer de uretra"),
        models.Diagnosis(name="Cáncer de vejiga"),
        models.Diagnosis(name="Candidiasis"),
        models.Diagnosis(name="Cardiopatías congénitas"),
        models.Diagnosis(name="Cataratas"),
        models.Diagnosis(name="Celiaquía"),
        models.Diagnosis(name="Cervicitis"),
        models.Diagnosis(name="Chikungunya"),
        models.Diagnosis(name="Ciática"),
        models.Diagnosis(name="Cirrosis"),
        models.Diagnosis(name="Citomegalovirus"),
        models.Diagnosis(name="Colecistitis"),
        models.Diagnosis(name="Colelitiasis"),
        models.Diagnosis(name="Cólera"),
        models.Diagnosis(name="Cólico del lactante"),
        models.Diagnosis(name="Cólico nefrótico"),
        models.Diagnosis(name="Colitis ulcerosa"),
        models.Diagnosis(name="Colon irritable"),
        models.Diagnosis(name="Conjuntivitis"),
        models.Diagnosis(name="Coronavirus"),
        models.Diagnosis(name="Corte de digestión o hidrocución"),
        models.Diagnosis(name="Creutzfeldt jakob (Vacas locas)"),
        models.Diagnosis(
            name="Degeneración macular asociada a la edad (DMAE)"),
        models.Diagnosis(name="Demencia"),
        models.Diagnosis(name="Demencia con cuerpos de Lewy"),
        models.Diagnosis(name="Dengue"),
        models.Diagnosis(name="Depresión"),
        models.Diagnosis(name="Dermatitis atípica"),
        models.Diagnosis(name="Dermatitis del pañal"),
        models.Diagnosis(name="Dermatitis seborreica"),
        models.Diagnosis(name="Derrame pleural"),
        models.Diagnosis(name="Desprendimiento de retina"),
        models.Diagnosis(name="Diabetes"),
        models.Diagnosis(name="Diarrea"),
        models.Diagnosis(name="Diarrea del viajero"),
        models.Diagnosis(name="Difteria"),
        models.Diagnosis(name="Disfunción sexual femenina"),
        models.Diagnosis(name="Dislexia"),
        models.Diagnosis(name="Dismenorrea"),
        models.Diagnosis(name="Dismorfofobia"),
        models.Diagnosis(name="Dispepsia"),
        models.Diagnosis(name="Diverticulitis"),
        models.Diagnosis(name="Dolor de cabeza o cefalea"),
        models.Diagnosis(name="Eccema"),
        models.Diagnosis(name="Edema Pulmonar"),
        models.Diagnosis(name="ELA (esclerosis lateral amiotrófica)"),
        models.Diagnosis(name="Embolia pulmonar"),
        models.Diagnosis(name="Encefalitis"),
        models.Diagnosis(name="Encefalopatía hepática"),
        models.Diagnosis(name="Endocarditis"),
        models.Diagnosis(name="Endometriosis"),
        models.Diagnosis(name="Enfermedad de Crohn"),
        models.Diagnosis(name="Enfermedad de Kawasaki"),
        models.Diagnosis(name="Enfermedad de Paget"),
        models.Diagnosis(name="Enfermedad de Whipple"),
        models.Diagnosis(name="Enfermedad de Wilson"),
        models.Diagnosis(name="Enfermedad del sueño"),
        models.Diagnosis(name="Enfermedad por virus de Marburgo"),
        models.Diagnosis(name="Enfermedad renal crónica"),
        models.Diagnosis(name="Enfermedad tromboembólica venosa"),
        models.Diagnosis(name="Enfisema"),
        models.Diagnosis(name="Enuresis"),
        models.Diagnosis(name="Epilepsia"),
        models.Diagnosis(
            name="EPOC (enfermedad pulmonar obstructiva crónica)"),
        models.Diagnosis(name="Escarlatina"),
        models.Diagnosis(name="Esclerodermia"),
        models.Diagnosis(name="Esclerosis múltiple"),
        models.Diagnosis(name="Escoliosis"),
        models.Diagnosis(name="Esofagitis"),
        models.Diagnosis(name="Esofagitis eosinofólica"),
        models.Diagnosis(name="Esófago de Barret"),
        models.Diagnosis(name="Espina bífida"),
        models.Diagnosis(name="Espolón calcáneo"),
        models.Diagnosis(name="Espondilitis anquilosante"),
        models.Diagnosis(name="Esquizofrenia"),
        models.Diagnosis(name="Esterilidad e infertilidad"),
        models.Diagnosis(name="Estrabismo"),
        models.Diagnosis(name="Estreñimiento"),
        models.Diagnosis(name="Estrés"),
        models.Diagnosis(name="Factores de riesgo cardiovascular"),
        models.Diagnosis(name="Faringitis"),
        models.Diagnosis(name="Faringoamigdalitis"),
        models.Diagnosis(name="Fascitis plantar"),
        models.Diagnosis(name="Fenilcetonuria"),
        models.Diagnosis(name="Fibromialgia"),
        models.Diagnosis(name="Fibrosis pulmonar"),
        models.Diagnosis(name="Fibrosis pulmonar idiopática"),
        models.Diagnosis(name="Fibrosis Quística"),
        models.Diagnosis(name="Fiebre amarilla"),
        models.Diagnosis(name="Fiebre del heno"),
        models.Diagnosis(name="Fiebre tifoidea"),
        models.Diagnosis(name="Fiebres hemorrágicas"),
        models.Diagnosis(name="Fimosis"),
        models.Diagnosis(name="Fobia social"),
        models.Diagnosis(name="Gases y flatulencias"),
        models.Diagnosis(name="Gastritis"),
        models.Diagnosis(name="Gastroenteritis"),
        models.Diagnosis(name="Glaucoma"),
        models.Diagnosis(name="Golpe de calor"),
        models.Diagnosis(name="Gonorrea"),
        models.Diagnosis(name="Gota"),
        models.Diagnosis(name="Gripe"),
        models.Diagnosis(name="Hafefobia"),
        models.Diagnosis(name="Halitosis"),
        models.Diagnosis(name="Hematoma subdural"),
        models.Diagnosis(name="Hemocromatosis"),
        models.Diagnosis(name="Hemofilia"),
        models.Diagnosis(name="Hemorragias ginecológicas"),
        models.Diagnosis(name="Hemorroides"),
        models.Diagnosis(name="Hepatitis A"),
        models.Diagnosis(name="Hepatitis B"),
        models.Diagnosis(name="Hepatitis C"),
        models.Diagnosis(name="Hernia discal"),
        models.Diagnosis(name="Hernia inguinal"),
        models.Diagnosis(name="Herpes labial"),
        models.Diagnosis(name="Herpes zóster"),
        models.Diagnosis(name="Hidradenitis supurativa"),
        models.Diagnosis(name="Hidrocele"),
        models.Diagnosis(name="Hipercolesterolemia"),
        models.Diagnosis(name="Hipercolesterolemia familiar"),
        models.Diagnosis(name="Hiperhidrosis"),
        models.Diagnosis(name="Hipermenorrea"),
        models.Diagnosis(name="Hipermetropía"),
        models.Diagnosis(name="Hiperplasia benigna de próstata"),
        models.Diagnosis(name="Hipertensión arterial"),
        models.Diagnosis(name="Hipertiroidismo"),
        models.Diagnosis(name="Hipoglucemia"),
        models.Diagnosis(name="Hipotensión"),
        models.Diagnosis(name="Hipotiroidismo"),
        models.Diagnosis(name="Hirsutismo"),
        models.Diagnosis(name="Hongos"),
        models.Diagnosis(name="Ictus"),
        models.Diagnosis(name="Impétigo"),
        models.Diagnosis(name="Impotencia/ disfunción eréctil"),
        models.Diagnosis(name="Incontinencia urinaria"),
        models.Diagnosis(name="Infarto de miocardio"),
        models.Diagnosis(name="Infección urinaria o cistitis"),
        models.Diagnosis(name="Insomnio"),
        models.Diagnosis(name="Insuficiencia cardiaca"),
        models.Diagnosis(name="Intolerancia a la lactosa"),
        models.Diagnosis(name="Juanetes"),
        models.Diagnosis(name="Ladillas (piojos del pubis)"),
        models.Diagnosis(name="Legionella"),
        models.Diagnosis(name="Leishmaniasis"),
        models.Diagnosis(
            name="Lengua geográfica o glositis migratoria benigna"),
        models.Diagnosis(name="Lepra"),
        models.Diagnosis(name="Leucemia"),
        models.Diagnosis(name="Linfoma"),
        models.Diagnosis(name="Lipedema"),
        models.Diagnosis(name="Lipotimia"),
        models.Diagnosis(name="Listeriosis"),
        models.Diagnosis(name="Litiasis renal"),
        models.Diagnosis(name="Ludopatía"),
        models.Diagnosis(name="Lumbalgia"),
        models.Diagnosis(name="Lupus"),
        models.Diagnosis(name="Malaria"),
        models.Diagnosis(name="Melanoma"),
        models.Diagnosis(name="Melanoma metastásico"),
        models.Diagnosis(name="Melasma"),
        models.Diagnosis(name="Meningitis"),
        models.Diagnosis(name="Mielitis transversa"),
        models.Diagnosis(name="Mieloma múltiple"),
        models.Diagnosis(name="Migrañas"),
        models.Diagnosis(name="Miocardiopatía"),
        models.Diagnosis(name="Miomas uterinos"),
        models.Diagnosis(name="Miopía"),
        models.Diagnosis(name="Mobbing"),
        models.Diagnosis(name="Molusco contagioso"),
        models.Diagnosis(name="Mononucleosis"),
        models.Diagnosis(name="Muerte súbita cardiaca"),
        models.Diagnosis(name="Narcolepsia"),
        models.Diagnosis(name="Neumonía"),
        models.Diagnosis(name="Neumotórax"),
        models.Diagnosis(name="Obesidad"),
        models.Diagnosis(name="Ojo seco"),
        models.Diagnosis(name="Ojo vago"),
        models.Diagnosis(name="Orquitis"),
        models.Diagnosis(name="Ortorexia"),
        models.Diagnosis(name="Orzuelo"),
        models.Diagnosis(name="Osteoporosis"),
        models.Diagnosis(name="Osteosarcoma"),
        models.Diagnosis(name="Otitis"),
        models.Diagnosis(name="Pancreatitis"),
        models.Diagnosis(name="Paperas (parotiditis)"),
        models.Diagnosis(name="Parálisis de Bell"),
        models.Diagnosis(name="Parálisis del sueño"),
        models.Diagnosis(name="Parkinson"),
        models.Diagnosis(name="Pericarditis"),
        models.Diagnosis(name="Peste"),
        models.Diagnosis(name="Pie de atleta"),
        models.Diagnosis(name="Pielonefritis"),
        models.Diagnosis(name="Pies cavos"),
        models.Diagnosis(name="Pies planos"),
        models.Diagnosis(name="Pies zambos"),
        models.Diagnosis(name="Poliomielitis"),
        models.Diagnosis(name="Preeclampsia"),
        models.Diagnosis(name="Presbicia"),
        models.Diagnosis(name="Prostatitis"),
        models.Diagnosis(name="Psoriasis"),
        models.Diagnosis(name="Rabia"),
        models.Diagnosis(name="Rectocele"),
        models.Diagnosis(name="Retinoblastoma"),
        models.Diagnosis(name="Retinopatía diabética"),
        models.Diagnosis(name="Rinitis"),
        models.Diagnosis(name="Rosácea"),
        models.Diagnosis(name="Rotavirus"),
        models.Diagnosis(name="Rubéola"),
        models.Diagnosis(name="Salmonelosis"),
        models.Diagnosis(name="Sarampión"),
        models.Diagnosis(name="Sarcoidosis"),
        models.Diagnosis(name="Sarcoma"),
        models.Diagnosis(name="Sepsis"),
        models.Diagnosis(name="Sífilis"),
        models.Diagnosis(name="Silicosis"),
        models.Diagnosis(name="Síndrome de burnout"),
        models.Diagnosis(name="Síndrome de Diógenes"),
        models.Diagnosis(name="Síndrome de Down"),
        models.Diagnosis(name="Síndrome de Dravet"),
        models.Diagnosis(name="Síndrome de estrés postraumático"),
        models.Diagnosis(name="Síndrome de fatiga crónica"),
        models.Diagnosis(name="Síndrome de Ganser"),
        models.Diagnosis(name="Síndrome de Gilbert"),
        models.Diagnosis(name="Síndrome de Gorlin-Goltz"),
        models.Diagnosis(name="Síndrome de Guillain-Barré"),
        models.Diagnosis(name="Síndrome de hiperestimulación ovárica"),
        models.Diagnosis(name="Síndrome de Marfan"),
        models.Diagnosis(name="Síndrome de Patau"),
        models.Diagnosis(name="Síndrome de Reiter"),
        models.Diagnosis(name="Síndrome de Rett"),
        models.Diagnosis(name="Síndrome de Reye"),
        models.Diagnosis(name="Síndrome de Sanfilippo"),
        models.Diagnosis(name="Síndrome de Sjögren"),
        models.Diagnosis(name="Síndrome de Smith-Magenis"),
        models.Diagnosis(name="Síndrome de Tourette"),
        models.Diagnosis(name="Síndrome de Turner"),
        models.Diagnosis(name="Síndrome de Williams"),
        models.Diagnosis(name="Síndrome de Wolfram"),
        models.Diagnosis(name="Síndrome del túnel carpiano"),
        models.Diagnosis(name="Síndrome postvacacional"),
        models.Diagnosis(name="Síndromes mielodisplásicos (SMD)"),
        models.Diagnosis(name="Sinus Pilonidal"),
        models.Diagnosis(name="Sinusitis"),
        models.Diagnosis(name="Siringomielia"),
        models.Diagnosis(name="Sobrecrecimiento bacteriano o SIBO"),
        models.Diagnosis(name="Sonambulismo"),
        models.Diagnosis(name="Tendinitis"),
        models.Diagnosis(name="Tétanos"),
        models.Diagnosis(name="Tortícolis"),
        models.Diagnosis(name="Tos ferina"),
        models.Diagnosis(name="Toxoplasmosis"),
        models.Diagnosis(name="Trastorno bipolar"),
        models.Diagnosis(name="Trastorno de conducta del sueño en fase REM"),
        models.Diagnosis(name="Trastorno de menstruación"),
        models.Diagnosis(name="Trastorno obsesivo compulsivo (TOC)"),
        models.Diagnosis(name="Trastorno por atracón"),
        models.Diagnosis(
            name="Trastorno por déficit de atención e hiperactividad (TDAH)"),
        models.Diagnosis(name="Trastornos del ritmo circadiano"),
        models.Diagnosis(name="Tricomoniasis"),
        models.Diagnosis(name="Trombosis venosa (flebitis)"),
        models.Diagnosis(name="Tuberculosis"),
        models.Diagnosis(name="Tumores cerebrales"),
        models.Diagnosis(name="Uñas encarnadas (onicocriptosis)"),
        models.Diagnosis(name="Uretritis"),
        models.Diagnosis(name="Urticaria"),
        models.Diagnosis(name="Vaginitis o vulvovaginitis"),
        models.Diagnosis(name="Vaginosis bacteriana"),
        models.Diagnosis(name="Varicela"),
        models.Diagnosis(name="Varices"),
        models.Diagnosis(name="Varicocele"),
        models.Diagnosis(name="Vasculitis"),
        models.Diagnosis(name="Vegetaciones"),
        models.Diagnosis(name="Vértigo"),
        models.Diagnosis(name="Vigorexia"),
        models.Diagnosis(name="VIH / Sida"),
        models.Diagnosis(name="Virus del Nilo Occidental"),
        models.Diagnosis(name="Virus del papiloma humano (VPH)"),
        models.Diagnosis(name="Virus Zika"),
        models.Diagnosis(name="Vitíligo"),
        models.Diagnosis(name="Vulvitis")
    ]

    db.bulk_save_objects(diagnosis)

    # Tipos de estudio

    with open('/app/templates/study_types/exoma.html', 'r') as file:
        exoma = file.read().replace('\n', '')
    with open('/app/templates/study_types/genoma.html', 'r') as file:
        genoma = file.read().replace('\n', '')
    with open('/app/templates/study_types/carrier.html', 'r') as file:
        carrier = file.read().replace('\n', '')
    with open('/app/templates/study_types/cariotipo.html', 'r') as file:
        cariotipo = file.read().replace('\n', '')
    with open('/app/templates/study_types/array.html', 'r') as file:
        array = file.read().replace('\n', '')

    db.add(models.TypeStudy(
        name="Exoma",
        study_consent_template=exoma))
    db.add(models.TypeStudy(
        name="Genoma mitoclondrial completo",
        study_consent_template=genoma))
    db.add(models.TypeStudy(
        name="Carrier",
        study_consent_template=carrier))
    db.add(models.TypeStudy(
        name="Cariotipo",
        study_consent_template=cariotipo))
    db.add(models.TypeStudy(
        name="Array CGH",
        study_consent_template=array))

    db.commit()
