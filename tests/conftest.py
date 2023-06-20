import pytest

from unittest.mock import MagicMock

from models import Student
from app import app


@pytest.fixture
def conn_mock(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr("utils.db_utils.db_connect", MagicMock(return_value=conn))
    return conn


@pytest.fixture
def student_data():
    return {
        "group_id": 1,
        "first_name": "Guido",
        "last_name": "Rossum"
    }


@pytest.fixture
def student_with_empty_data():
    return {
        "group_id": 1,
        "first_name": "",
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
