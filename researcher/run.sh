#! /bin/bash

set -e # fail fast

TOPICS=$1

poetry run researcher --topics-filepath $TOPICS
echo "Finished."