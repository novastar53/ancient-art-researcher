#! /bin/bash

set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

TOPICS=$1

poetry run researcher --topics-filepath $TOPICS
echo "Finished."