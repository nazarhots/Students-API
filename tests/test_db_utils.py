from unittest.mock import MagicMock
from db_utils import db_connect, execute_sql_file


def test_db_connect(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr("db_utils.psycopg2.connect", MagicMock(return_value=conn))

    result = db_connect()

    assert result == conn 


def test_execute_sql_file(tmp_path, conn_mock):
    test_sql = """
    CREATE TABLE test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    """
    sql_file = tmp_path / "test.sql"
    sql_file.write_text(test_sql)
    execute_sql_file(str(sql_file))

    conn_mock.cursor.assert_called_once()
    conn_mock.commit.assert_called_once()
    conn_mock.close.assert_called_once()

    conn_mock.close()
    

def test_execute_sql_file_with_error(conn_mock):
    result = execute_sql_file("path_to_file")
    
    assert "Error" in result
