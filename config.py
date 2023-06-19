import os

from dotenv import load_dotenv


load_dotenv()

# DB data
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# Paths
create_table_path = os.getenv("CREATE_TABLE_PATH")
logger_path = os.getenv("LOGGER_PATH")

# Config
app_server_name = os.getenv("APP_SERVER_NAME")
