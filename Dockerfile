FROM python:3.8.3-slim

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code/

COPY Pipfile* /code/

RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile


COPY . /code
