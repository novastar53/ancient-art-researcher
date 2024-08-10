#! /bin/bash

set -e # fail fast

TOPICS=$1

while IFS= read -r line
do
    echo $line
    poetry run researcher "$line"
done < $TOPICS