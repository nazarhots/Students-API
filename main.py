from utils.db_utils import execute_sql_file, generate_db_data
from config import create_table_path
from app import app


if __name__ == "__main__":
    execute_sql_file(create_table_path)
    generate_db_data()
    app.run()
    