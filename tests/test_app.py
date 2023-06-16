from unittest.mock import patch

from flask import url_for

from models import Student


@patch("app.session.query")
@patch("app.paginate")
def test_studentslistresource_get(mock_paginate, mock_query, client):
    mock_result = [
        Student(id=1, group_id=1, first_name="Some", last_name="Name"),
        Student(id=2, group_id=2, first_name="Another", last_name="Name"),
    ]
    expected_result = [
        {"first_name": "Some", "group_id": 1, "id": 1, "last_name": "Name"},
        {"first_name": "Another", "group_id": 2, "id": 2, "last_name": "Name"}
    ]
    mock_query.return_value = mock_result
    mock_paginate.return_value.items = mock_result

    response = client.get(url_for("studentslistresource"))

    assert response.status_code == 200
    assert response.json == expected_result


@patch("app.session.query", return_value=Exception)
def test_studentslistresource_get_error(mock_query, client):
    response = client.get(url_for("studentslistresource"))

    assert response.status_code == 500
    assert "Error" in response.text


@patch("app.session.add")
def test_studentslistresource_post(mock_add, student_data, client):
    response = client.post(url_for("studentslistresource"), json=student_data)

    assert response.status_code == 200
    mock_add.assert_called_once()


@patch("app.session.add", side_effect=Exception)
def test_studentslistresource_post_error(mock_add, client, student_data):
    response = client.post(url_for("studentslistresource"), json=student_data)

    assert response.status_code == 500
    assert "Error" in response.json


@patch("app.session.query")
def test_studentresource_put(mock_query, student, student_data, client):
    mock_query.return_value.get.return_value = student

    response = client.put(url_for("studentresource", student_id=1), json=student_data)

    assert response.status_code == 200
    assert "Student with ID 1 updated successfully" in response.text


@patch("app.session.query", return_value={})
def test_studentresource_put_id_not_found(mock_query, client, student_data):
    response = client.put(url_for("studentresource", student_id=234), json=student_data)

    assert "Student with ID 234 not found" in response.text


@patch("app.session.add", return_value = Exception)
def test_studentresource_put_error(mock_add, client, student_data):
    response = client.put(url_for("studentresource", student_id=123), json=student_data)

    assert response.status_code == 500
    assert "Error" in response.json


@patch("app.session.delete")
@patch("app.session.query")
def test_studentresource_delete(mock_query, mock_delete, client):
    response = client.delete(url_for("studentresource", student_id=1))

    assert response.status_code == 200
    assert f"Student with ID 1 deleted successfully" in response.text


@patch("app.session.query", return_value={})
def test_studentresource_delete_id_not_found(mock_query, client):
    response = client.delete(url_for("studentresource", student_id=234))

    assert "Student with ID 234 not found" in response.text


@patch("app.session.query", return_value=Exception)
def test_studentresource_delete_error(mock_query, client):
    response = client.delete(url_for("studentresource", student_id=234))

    assert response.status_code == 500
    assert "Error" in response.json
