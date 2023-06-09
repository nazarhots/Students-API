from db_utils import execute_sql_file, generate_db_data
from config import create_table_path


if __name__ == "__main__":
    execute_sql_file(create_table_path)
    generate_db_data()