FROM --platform=linux/amd64 python:3.12-slim as build

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./src/finds_viewer/. . 
COPY ".env" .
COPY pyproject.toml poetry.lock ./
COPY google-service-account.json .

RUN poetry install --only main

CMD ["python", "app.py"]
