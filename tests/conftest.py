import pytest

from unittest.mock import MagicMock, patch

from models import Student
from app import app


@pytest.fixture
def conn_mock(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr("db_utils.db_connect", MagicMock(return_value=conn))
    return conn


@pytest.fixture
def student_data():
    return {
        "group_id": 1,
        "first_name": "Guido",
        "last_name": "Rossum"
    }


@pytest.fixture
def student():
    return Student(id=1, group_id=1, first_name="Anders", last_name="Hejlsberg")


@pytest.fixture
def client():
    with app.test_request_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def client_get_json_exeption():
    with app.test_request_context():
        with patch("app.request.get_json", return_value=Exception):
            with app.test_client() as client:
                yield client
                
@pytest.fixture
def client_get_json_with_student_data():
    with app.test_request_context():
        with patch("app.request.get_json", return_value={
                                            "group_id": 1,
                                            "first_name": "Guido",
                                            "last_name": "Rossum"
                                        }):
            with app.test_client() as client:
                yield client