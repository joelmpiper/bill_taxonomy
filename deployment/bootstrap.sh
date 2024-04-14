#!/bin/bash
# bootstrap.sh

# Load the environment from config.yml
ENVIRONMENT=$(yq e '.environment' ../configs/postgres_setup.yml)

# move into base environment
cd ..

# Export the appropriate environment variables from the .env file
if [ "$ENVIRONMENT" = "development" ]; then
  while IFS='=' read -r name value
  do
    # Remove the DEV_ prefix and export
    export ${name#DEV_}=$value
  done < <(grep 'DEV_' .env)
elif [ "$ENVIRONMENT" = "production" ]; then
  while IFS='=' read -r name value
  do
    # Remove the PROD_ prefix and export
    export ${name#PROD_}=$value
  done < <(grep 'PROD_' .env)
fi

# Navigate to the directory containing docker-compose.yml
cd deployment

# Rebuild without cache
docker-compose build --no-cache

# Now run Docker Compose
docker-compose up -d
