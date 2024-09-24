#! /bin/bash

set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT/finds-viewer:latest .