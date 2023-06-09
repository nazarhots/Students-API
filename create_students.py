import string
import random

from names import get_full_name
import sqlalchemy.exc

from models import Student, Group, Course


def generate_group_name() -> str:
    """
    Generates a random group name.

    Example:
        AA-02
        BE-53
        JF-15
    """
    letters = "".join(random.choice(string.ascii_uppercase) for _ in range(2))
    number = "{:02d}".format(random.randrange(1, 99))
    group_name = f"{letters}-{number}"
    return group_name
    
    
def courses_description() -> dict:
    courses = {
        "Mathematics": "Study of numbers, quantity, and space",
        "Computer Science": "Study of computation and information processing",
        "English": "Study of the English language and literature",
        "History": "Study of past events and their significance",
        "Geography": "Study of the Earth's physical features and atmosphere",
        "Physics": "Study of matter, energy, and the interactions between them",
        "Chemistry": "Study of substances, their properties, and transformations",
        "Biology": "Study of living organisms and their vital processes",
        "Art": "Study of creative expression and visual communication",
        "Health Education": "Study of health-related topics and promoting well-being"
    }
    return courses


def generate_full_name() -> str:
    return get_full_name()


def create_groups(number: int = 10) -> list[Group]:
    """
    Creates a list of groups.

    Args:
        number (int, optional): The number of groups to create. Defaults to 10.
    """
    try:
        groups = [Group(name=generate_group_name()) for _ in range(number)]
        return groups
    except sqlalchemy.exc.SQLAlchemyError as error:
        raise Exception(f"Error during creating groups: {error}")


def create_courses() -> list[Course]:
    try:
        courses = [Course(name=course_name, description=description) for course_name, description in courses_description().items()]
        return courses
    except sqlalchemy.exc.SQLAlchemyError as error:
        raise Exception(f"Error during creating courses: {error}")


def create_students(number: int = 200) -> list[Student]:
    """
    Creates a list of students.

    Args:
        number (int, optional): The number of students to create. Defaults to 200.
    """
    try:
        students = []
        for _ in range(number):
            full_name = generate_full_name()
            first_name, last_name = full_name.split()
            students.append(Student(first_name=first_name, last_name=last_name))
        return students
    except sqlalchemy.exc.SQLAlchemyError as error:
        raise Exception(f"Error during creating students: {error}")
