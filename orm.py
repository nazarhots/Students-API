from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import OperationalError

from models import Student, Group, Course, StudentCourse
from app import session


def find_groups_by_student_count(number: int = 10):
    """
    Find groups with less or equal number of students.
    
    Args:
        number (int): Maximum number of students in a group (default is 10).
    """
    try:
        groups = (
            session.query(Group)
            .join(Group.students)
            .group_by(Group.id)
            .having(func.count(Student.id) <= number)
            .all()
        )
        return groups
    except (SQLAlchemyError, OperationalError):
        raise


def find_students_by_course_name(course_name: str):
    """
    Find students related to a course by its name.
    
    Args:
        course_name (str): Name of the course.
    """
    try:
        students = (
            session.query(Student)
            .join(Student.enrolled_courses)
            .join(StudentCourse.course)
            .filter(Course.name == course_name)
            .all()
        )
        return students
    except (SQLAlchemyError, OperationalError):
        raise


def add_new_student(group_id, first_name, last_name):
    """
    Add a new student.
    
    Args:
        group_id (int): ID of the group the student belongs to.
        first_name (str): First name of the student.
        last_name (str): Last name of the student.
    """
    try:
        student = Student(
            group_id=group_id,
            first_name=first_name,
            last_name=last_name
        )
        session.add(student)
        session.commit()
        return True
    except (SQLAlchemyError, OperationalError):
        raise


def delete_student_by_id(student_id: int):
    """
    Delete a student by their ID.
    
    Args:
        student_id (int): ID of the student.
    """
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student with ID {student_id} not found")
        session.delete(student)
        session.commit()
        return True
    except (SQLAlchemyError, OperationalError):
        raise


def add_student_to_course(student_id: int, course_id: int):
    """
    Add a student to a course.
    
    Args:
        student_id (int): ID of the student.
        course_id (int): ID of the course.
    """
    try:
        student = session.query(StudentCourse).filter(StudentCourse.student_id == student_id).first()
        course = session.query(StudentCourse).filter(StudentCourse.course_id == course_id).first()
        student_in_course = (
            session.query(StudentCourse)
            .filter(StudentCourse.student_id == student_id, StudentCourse.course_id == course_id)
            .all()
        )
        if not student or not course:
            raise ValueError("Invalid data. Please check student ID and course ID")
        if student_in_course:
            raise ValueError("Student already in this course")
        student_course = StudentCourse(student_id=student_id, course_id=course_id)
        session.add(student_course)
        session.commit()
        return True
    except (SQLAlchemyError, OperationalError):
        raise


def delete_student_from_course(student_id: int, course_id: int):
    """
    Remove a student from a course.
    
    Args:
        student_id (int): ID of the student.
        course_id (int): ID of the course.
    """
    try:
        student = session.query(StudentCourse).filter(StudentCourse.student_id == student_id, StudentCourse.course_id == course_id).first()
        if not student:
            raise ValueError("Invalid data. Please check student ID and course ID")
        session.delete(student)
        session.commit()
        return True
    except (SQLAlchemyError, OperationalError):
        raise
