FROM --platform=linux/amd64 python:3.12-slim as build

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV GOOGLE_APPLICATION_CREDENTIALS "google-service-account.json"
ENV BUCKET_NAME "latest-finds-images-happy-cat-234"

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./src/. . 
COPY pyproject.toml .
COPY google-service-account.json .

RUN poetry install --no-dev

CMD ["python", "app.py"]
