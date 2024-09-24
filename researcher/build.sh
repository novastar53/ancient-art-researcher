set -e # fail fast

docker build --platform linux/amd64  --build-arg GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS -t gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest .
