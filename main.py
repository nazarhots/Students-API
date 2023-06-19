from sqlalchemy import inspect

from utils.db_utils import execute_sql_file, generate_db_data
from config import create_table_path
from app import app, create_database_engine


def tables_exist():
    inspector = inspect(create_database_engine())
    table_names = inspector.get_table_names()
    return len(table_names) > 0


if __name__ == "__main__":
    if not tables_exist():
        execute_sql_file(create_table_path)
        generate_db_data()
    app.run()
