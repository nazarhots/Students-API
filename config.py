import os

from dotenv import load_dotenv


load_dotenv()

# DB data
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_DB_HOST")
port = os.getenv("POSTGRES_DB_PORT")

# Paths
create_table_path = os.getenv("CREATE_TABLE_PATH")
logger_path = os.getenv("LOGGER_PATH")

# Config
app_server_name = os.getenv("APP_SERVER_NAME")

# Constants
MAX_DB_RETRIES = 3
RETRIES_SLEEP_INTERVAL = 1
