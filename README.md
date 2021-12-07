# TTPS2021 Backend
TTPS 2021 grupo 8
### Pasos (Completar)

Primero crear en la carpeta raiz del proyecto el archivo .env con al menos estos valores:

```
PROJECT_NAME=ttps-grupo8

SERVER_HOST=http://localhost
ADMIN_USERNAME=changeme
ADMIN_PASSWORD=changeme

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme
POSTGRES_DB=ttps-grupo8

# PgAdmin
PGADMIN_DEFAULT_EMAIL=pgadmin4@pgadmin.org
PGADMIN_DEFAULT_PASSWORD=changeme
PGADMIN_CONFIG_SERVER_MODE=False

# To avoid scopes validation
DEVELOPMENT=True

# to send mails
MAIL_USERNAME=<MAIL_USERNAME>
MAIL_PASSWORD=<MAIL_PASSWORD>
MAIL_FROM=<SENDER_ADDRESS>
MAIL_PORT=<MAIL_PORT>
MAIL_SERVER=<MAIL_SERVER>
MAIL_FROM_NAME=<TITLE_FOR_MAIL>
```


Abrir una terminal en la misma ruta y ejecutar:

```
docker-compose up -d
```

Luego:

```
docker-compose exec backend bash
```

dentro del contenedor:

```
bash startup.sh
```

Si todo salió bien, se puede acceder a la documentación de la api:

```
http://localhost:8000/docs
```

Y también visualizar y modificar la base de datos median pgAdmin (ingresando las credenciales definidas en el archivo `.env` para las variables de entorno `PGADMIN_DEFAULT_EMAIL` y `PGADMIN_DEFAULT_PASSWORD` respectivamente):

```
http://localhost:5050
```

## Sección para desarrolladores del backend

### Actualizar imagen del backend

Para el caso en que se quiera agregar un paquete, una vez dentro del contenedor del backend ejecutar:
```
poetry add nombre-del-paquete
```
si todo salió correctamnete, el comando anterior modificó los archivos asociados a poetry que se encuentran
dentro de la carpeta `backend`. Lo que restaría es construir nuevamente la imagen del docker del backend:
```
docker-compose build backend
```
### Migrations

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in the database. Otherwise, the application will have errors.

* As an example, if you created a new model in `./backend/app/models/`, make sure to import it in `./backend/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```
