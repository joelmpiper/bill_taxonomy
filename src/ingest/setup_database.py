import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Base and table classes
Base = declarative_base()
from table_definitions import NewYorkBills, UsBills, BillSubjects  # Assuming these are defined in table_definitions.py

def load_config():
    # Adjust the path if needed to match the Docker container's directory structure
    config_path = '/code/configs/postgres_setup.yml'  # Example path inside Docker
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def make_database():
    config = load_config()

    # Print all environment variables
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    # Directly use environment variables, no prefix needed
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'postgres')  # Default to 'postgres' if not set
    port = os.getenv('DB_PORT', '5432')  # Default port if not set
    dbname = os.getenv('DB_NAME')
    db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    try:
        engine = create_engine(db_url)

        if not database_exists(engine.url):
            create_database(engine.url)
            logging.info(f"Database {dbname} created successfully.")

        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)()
        for table_name, create in config['tables'].items():
            if create:
                class_ = globals()[table_name]
                class_.__table__.create(bind=engine, checkfirst=True)
                logging.info(f"Table {table_name} created successfully.")
        session.commit()
        session.close()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    make_database()