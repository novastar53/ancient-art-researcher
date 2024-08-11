#! /bin/bash

set -e # fail fast

# Load the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

TOPICS=$1

while IFS= read -r line
do
    echo $line
    poetry run researcher "$line"
    sleep 10
done < $TOPICS