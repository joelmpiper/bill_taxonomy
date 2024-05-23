#!/bin/bash

# Load the environment from config.yml
export ENVIRONMENT=$(yq e '.environment' ../configs/postgres_setup.yml)
export LOCAL=$(yq e '.local' ../configs/postgres_setup.yml)


# Decide on the Compose file to use
COMPOSE_FILE="docker-compose.yml"
if [ "$LOCAL" = "true" ]; then
    COMPOSE_FILE="${COMPOSE_FILE} -f docker-compose.local.yml"
fi

echo "LOCAL: $LOCAL"
echo "Using Compose File: $COMPOSE_FILE"
# Rebuild without cache
docker-compose -f $COMPOSE_FILE build --no-cache

# Now run Docker Compose
docker-compose -f $COMPOSE_FILE up -d --verbose
