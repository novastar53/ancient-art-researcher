set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest .
docker push gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest
# TODO: Run remotely on GCloud
#docker run gcr.io/history-research-assistant/researcher:latest
