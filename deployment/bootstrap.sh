#!/bin/bash

# Load the environment from config.yml
export ENVIRONMENT=$(yq e '.environment' ../configs/postgres_setup.yml)
export LOCAL=$(yq e '.local' ../configs/postgres_setup.yml)

# Set AWS_MOUNT if LOCAL is "true"
if [ "$LOCAL" = "true" ]; then
    export AWS_MOUNT="/Users/joeljoel/.aws:/root/.aws:ro"
else
    export AWS_MOUNT="/dev/null"
fi

# Rebuild without cache
docker-compose build --no-cache

# Now run Docker Compose
docker-compose up -d
