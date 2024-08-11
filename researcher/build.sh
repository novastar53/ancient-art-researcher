set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker build --build-arg GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS -t gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest .
docker push gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest
