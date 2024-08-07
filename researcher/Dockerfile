FROM python:3.12-slim 
#FROM --platform=linux/amd64 python:3.12-slim as build

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV GOOGLE_APPLICATION_CREDENTIALS "history-research-assistant-cc5c45e3ff39.json"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./src/. . 
COPY ".env" .
COPY history-research-assistant-cc5c45e3ff39.json .
COPY pyproject.toml .

RUN poetry install --only main

#RUN python researcher/manage_redis.py

CMD ["poetry", "run", "researcher"]
