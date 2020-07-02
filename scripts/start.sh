#!/bin/sh
pipenv run wait-for-it --service db:5432 -- echo "Postgres is up"
pipenv run alembic upgrade head
pipenv run uvicorn bank.main:app --host 0.0.0.0
