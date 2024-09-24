set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

docker push gcr.io/$GOOGLE_CLOUD_PROJECT/researcher:latest
gcloud run jobs describe researcher --region "$REGION" 
if [ $? -eq 0 ]; then
  gcloud run jobs update researcher --image gcr.io/$GOOGLE_CLOUD_PROJECT/researcher --memory 4Gi --region $REGION
else
  gcloud run jobs create researcher --image gcr.io/$GOOGLE_CLOUD_PROJECT/researcher --memory 4Gi --region $REGION 
fi
gcloud run jobs execute researcher --region $REGION