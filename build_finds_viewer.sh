docker build -t gcr.io/history-research-assistant/finds-viewer:latest .
docker push gcr.io/history-research-assistant/finds-viewer:latest
gcloud run deploy finds-viewer --image gcr.io/history-research-assistant/finds-viewer --platform managed --region us-east1 --allow-unauthenticated
