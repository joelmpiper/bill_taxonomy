#!/bin/bash

# Load the environment from config.yml
export ENVIRONMENT=$(yq e '.environment' ../configs/postgres_setup.yml)
export LOCAL=$(yq e '.local' ../configs/postgres_setup.yml)

# Set AWS_MOUNT if LOCAL is "true"
if [ "$LOCAL" = "true" ]; then
    export AWS_MOUNT="/Users/joeljoel/.aws:/root/.aws:ro"
else
    # Create an empty directory for AWS_MOUNT if necessary
    if [ ! -d "/tmp/aws-mount" ]; then
        mkdir -p /tmp/aws-mount
    fi
    export AWS_MOUNT="/tmp/aws-mount:/root/.aws:ro"  # Use the empty directory
fi

echo "LOCAL: $LOCAL"
echo "AWS_MOUNT: $AWS_MOUNT"
# Rebuild without cache
docker-compose build --no-cache

# Now run Docker Compose
docker-compose up -d --verbose
