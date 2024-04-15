import os
import logging
import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
import yaml

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='/code/logs/test_log.txt')

# Load Base and table classes
Base = declarative_base()
from table_definitions import NewYorkBills, UsBills, BillSubjects  # Assuming these are defined in table_definitions.py

def get_secret(secret_name):
    """Retrieve secret from AWS Secrets Manager."""
    region_name = os.getenv('AWS_REGION', 'us-east-1')  # Default to us-east-1 if not set

    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        logging.error(f"Error retrieving secret: {e}")
        return None

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    return None

def load_config():
    config_path = '/code/configs/postgres_setup.yml'
    with open(config_path, 'r') as file:
        config_raw = file.read()
        config = yaml.safe_load(config_raw)
        return config

def make_database():
    config = load_config()
    secret_name = config.get('aws_secret_name', 'default_secret_name_if_not_set')

    # Load secrets from AWS Secrets Manager
    secrets = get_secret(secret_name)
    user = secrets['username']
    password = secrets['password']
    host = secrets['host']
    port = secrets['port']
    dbname = secrets['dbname']

    db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    try:
        engine = create_engine(db_url)
        if not database_exists(engine.url):
            create_database(engine.url)
            logging.info(f"Database {dbname} created successfully.")
            print(f"Database {dbname} created successfully")
        
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)()
        for table_name, create in config['tables'].items():
            if create:
                class_ = globals()[table_name]
                class_.__table__.create(bind=engine, checkfirst=True)
                logging.info(f"Table {table_name} created successfully.")
                print(f"Table {table_name} created successfully.")
        session.commit()
        session.close()
        print("Closed session")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred {e}")

if __name__ == "__main__":
    make_database()
