FROM python:3.12-slim 

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Install the source separately to separate the dependencies layers from the source layers
COPY ./src/. . 
RUN poetry install --only main 

COPY ".env" .
ARG GOOGLE_APPLICATION_CREDENTIALS
COPY ${GOOGLE_APPLICATION_CREDENTIALS} .
COPY topics.txt .
COPY run.sh .

CMD ["./run.sh", "topics.txt"]
