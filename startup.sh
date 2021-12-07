#! /usr/bin/env bash

# Let the DB start
python app/backend_pre_start.py

status=$?

# Run migrations
alembic upgrade head

# Create initial data in DB

if (( status == 1 )); then #### status == 1 means that the db was just created (i know, it's ugly)
    echo "db created"
    python app/initial_data.py
fi


#Start app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir ./app
