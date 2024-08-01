FROM --platform=linux/amd64 python:3.8-slim as build
#FROM python:3.8-slim

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS "history-research-assistant-cc5c45e3ff39.json"
ENV BUCKET_NAME "latest-finds-images-happy-cat-234"

CMD ["python", "app.py"]
