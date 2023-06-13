import pytest

from unittest.mock import MagicMock

from models import Student


@pytest.fixture
def conn_mock(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr("db_utils.db_connect", MagicMock(return_value=conn))
    return conn


@pytest.fixture
def data():
    return {
        "group_id": 1,
        "first_name": "Guido",
        "last_name": "Rossum"
    }


@pytest.fixture
def student():
    return Student(id=1, group_id=1, first_name="Anders", last_name="Hejlsberg")
