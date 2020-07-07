# Bank
This is a simple banking app that allows create a new wallet, 
deposit it and transfer money between accounts.


## Deployment

    docker-compose up -d app

The app is running on http://localhost:8000/


## Run locally

Bring up PostgreSQL

    docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

set up the following environment variables

- POSTGRES_SERVER
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

for example

     export POSTGRES_SERVER=localhost
     export POSTGRES_USER=postgres
     export POSTGRES_PASSWORD=postgres
     export POSTGRES_DB=postgres

setup up virtual env using `pipenv`
    
    pip install pipenv
    pipenv install --dev

apply migrations

     alembic upgrade head

run webserver

    pipenv run uvicorn bank.main:app
    
## Run tests locally

    pipenv run pytest
