#! /bin/bash

set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker push gcr.io/$GOOGLE_CLOUD_PROJECT/finds-viewer:latest
gcloud run deploy finds-viewer --image gcr.io/$GOOGLE_CLOUD_PROJECT/finds-viewer --platform managed --region $REGION --allow-unauthenticated
