from unittest.mock import patch

from flask import url_for

from app import app
from models import Student
from config import app_server_name


app.config["SERVER_NAME"] = app_server_name

@patch("app.session.query")
@patch("app.paginate")
def test_get_all_students(mock_paginate, mock_query, client):
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

    response = client.get(url_for("get_all_students"))

    assert response.status_code == 200
    assert response.json == expected_result


@patch("app.session.query")
def test_get_all_students_exception(mock_query, client):
    mock_query.return_value = Exception("Some exception")

    response = client.get(url_for("get_all_students"))

    assert response.status_code == 500
    assert "Error" in response.text


@patch("app.session.add")
def test_create_student(mock_add, student_data, client):
    response = client.post(url_for("create_student"), json=student_data)

    assert response.status_code == 200


def test_create_student_error(client_get_json_exeption):
    response = client_get_json_exeption.post(url_for("create_student"))

    assert response.status_code == 500
    assert "Error" in response.json


@patch("app.session.query")
def test_update_student(mock_query, student, student_data, client_get_json_with_student_data):
    mock_query.return_value.get.return_value = student

    response = client_get_json_with_student_data.put(url_for("update_student", student_id=1), json=student_data)

    assert response.status_code == 200
    assert response.text == "Student with ID 1 updated successfully"


@patch("app.session.query")
def test_update_student_id_not_found(mock_query, client):
    mock_query.return_value = {}

    response = client.put(url_for("update_student", student_id=234))

    assert "Student with ID 234 not found" in response.text


def test_update_student_error(client_get_json_exeption):
    response = client_get_json_exeption.put(url_for("update_student", student_id=123))

    assert response.status_code == 500
    assert "Error" in response.json


@patch("app.session.delete")
@patch("app.session.query")
def test_delete_student(mock_query, mock_delete, client):
    response = client.delete(url_for("delete_student", student_id=1))

    assert response.status_code == 200
    assert response.text == f"Student with ID 1 deleted successfully"


@patch("app.session.query")
def test_delete_student_id_not_found(mock_query, client):
    mock_query.return_value = {}

    response = client.delete(url_for("delete_student", student_id=234))

    assert "Student with ID 234 not found" in response.text


@patch("app.session.query", return_value=Exception)
def test_delete_student_error(mock_query, client):
    response = client.delete(url_for("delete_student", student_id=234))

    assert response.status_code == 500
    assert "Error" in response.json
