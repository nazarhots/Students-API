import pytest
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import OperationalError

from unittest.mock import patch

from models import Student, Group, StudentCourse
from orm import find_groups_by_student_count, find_students_by_course_name, add_new_student, \
    delete_student_by_id, add_student_to_course, delete_student_from_course


@patch("app.session.query")
def test_find_groups_by_student_count(mock_query):
    test_data = [
        Group(id=1, name="Group 1"),
        Group(id=2, name="Group 2"),
    ]

    mock_query.return_value.join.return_value.group_by.return_value.having.return_value.all.return_value = test_data
    groups = find_groups_by_student_count()

    assert len(groups) == 2
    assert type(groups) == list
    mock_query.assert_called_once()
    
    
@patch("app.session.query")
def test_find_groups_by_student_count_sql_error(mock_query):
    mock_query.side_effect = SQLAlchemyError()
    with pytest.raises(SQLAlchemyError):
        find_groups_by_student_count()


@patch("app.session.query")
def test_find_students_by_course_name(mock_query):
    test_data = [
        Student(id=1, group_id=3, first_name="Bill", last_name="Gates"),
        Student(id=2, group_id=2, first_name="Ted", last_name="Codd"),
        ]
    mock_join = mock_query.return_value.join.return_value
    mock_filter = mock_join.join.return_value.filter.return_value
    mock_all = mock_filter.all

    mock_all.return_value = test_data
    students = find_students_by_course_name("Computer Science")
    
    assert len(students) == 2
    assert type(students) == list
    mock_query.assert_called_once()
    mock_query.return_value.join.assert_called_once_with(Student.enrolled_courses)
    mock_join.join.assert_called_once_with(StudentCourse.course)


@patch("app.session.query")
def test_find_students_by_course_name_sql_error(mock_query):
    mock_query.side_effect = SQLAlchemyError()
    with pytest.raises(SQLAlchemyError):
        find_students_by_course_name("Math")


@patch("app.session.add")
@patch("app.session.commit")
def test_add_new_student(mock_commit, mock_add):
    new_student = add_new_student(1, "James", "Gosling")

    assert new_student
    mock_add.assert_called_once()
    mock_commit.assert_called_once()


@patch("app.session.add")
def test_add_new_student_db_error(mock_add):
    mock_add.side_effect = OperationalError()
    with pytest.raises(OperationalError):
        add_new_student(1, "James", "Gosling")


@patch("app.session.delete")
@patch("app.session.commit")
@patch("app.session.query")
def test_delete_student_by_id(mock_query, mock_commit, mock_delete, student):
    mock_query.return_value.filter.return_value.first.return_value = student
    deleted_student = delete_student_by_id(1)
    
    assert deleted_student
    mock_delete.assert_called_once()
    mock_commit.assert_called_once()


@patch("app.session.query")
def test_delete_student_by_id_valuerrror(mock_query):
    mock_query.return_value.filter.return_value.first.return_value = []
    with pytest.raises(ValueError):
        delete_student_by_id(1)


@patch("app.session.query")
def test_delete_student_by_id_sql_error(mock_query):
    mock_query.side_effect = SQLAlchemyError()
    with pytest.raises(SQLAlchemyError):
        delete_student_by_id(1)


@patch("app.session.add")
@patch("app.session.commit")
@patch("app.session.query")
def test_add_student_to_course(mock_query, mock_commit, mock_add):
    mock_query.return_value.filter.return_value.first.return_value = ["Some data"]
    mock_query.return_value.filter.return_value.all.return_value = []
    student = add_student_to_course(1, 1)
    
    assert student
    mock_add.assert_called_once()
    mock_commit.assert_called_once()


@patch("app.session.query")
def test_add_student_to_course_invalid_data(mock_query):
    mock_query.return_value.filter.return_value.first.return_value = []
    with pytest.raises(ValueError):
        add_student_to_course(1, 1)


@patch("app.session.query")
def test_add_student_to_course_db_error(mock_query):
    mock_query.side_effect = OperationalError()
    with pytest.raises(OperationalError):
        add_student_to_course(1, 1)


@patch("app.session.delete")
@patch("app.session.commit")
@patch("app.session.query")
def test_delete_student_from_course(mock_query, mock_commit, mock_delete):
    mock_query.return_value.filter.return_value.first.return_value = ["Some data"]
    
    deleted_student = delete_student_from_course(1, 2)
    
    assert deleted_student
    mock_delete.assert_called_once()
    mock_commit.assert_called_once()
    
    
@patch("app.session.query")
def test_delete_student_from_course_invalid_data(mock_query):
    mock_query.return_value.filter.return_value.first.return_value = []
    with pytest.raises(ValueError):
        delete_student_from_course(1, 1)


@patch("app.session.query")
def test_delete_student_from_course_db_error(mock_query):
    mock_query.side_effect = OperationalError()
    with pytest.raises(OperationalError):
        delete_student_from_course(1, 1)
