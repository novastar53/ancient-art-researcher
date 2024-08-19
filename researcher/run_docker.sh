
# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker run gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest