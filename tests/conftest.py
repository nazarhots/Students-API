import pytest

from unittest.mock import MagicMock


@pytest.fixture
def conn_mock(monkeypatch):
    conn = MagicMock()
    monkeypatch.setattr('db_utils.db_connect', MagicMock(return_value=conn))
    return conn