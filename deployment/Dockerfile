# Use Python official image as the parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Install Poetry
RUN pip install poetry boto3

# Copy the Poetry configuration files specific to the ingest environment
COPY ../src/ingest/pyproject.toml ../src/ingest/poetry.lock* /code/

# Install dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the ingest specific Python scripts
COPY src/ingest/ /code/
COPY ../configs/postgres_setup.yml /code/configs/postgres_setup.yml

# Command to run on container start
CMD ["python", "setup_database.py"]
