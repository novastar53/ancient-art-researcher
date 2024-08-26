FROM --platform=linux/amd64 python:3.12-slim as build

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY ./src/finds_viewer/. . 
COPY ".env" .
RUN poetry install --only main

COPY google-service-account.json .

CMD ["python", "app.py"]
