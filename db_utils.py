import random
import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models import StudentCourse
from create_students import create_courses, create_groups, create_students
from config import dbname, user, password, host, port


def test():
    try:
        db_connect()
        print("Successfully connected to DB")

    except psycopg2.Error as e:
        print("Error:", e)


def db_connect():
    conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
    return conn


def execute_sql_file(file_path: str):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        with open(file_path, "r") as file:
            sql = file.read()
        cursor.execute(sql)
        conn.commit()
    except (psycopg2.Error, psycopg2.DatabaseError, FileNotFoundError) as error:
        return f"Error: {error}"
    finally:
        cursor.close()
        conn.close()


def create_database_engine():
    try:
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
        return engine
    except Exception as error:
        raise Exception(f"Error during creating engine: {error}")
    

def generate_db_data() -> None:
    """
    Generates data and inserts it into the database.
    """
    try:
        engine = create_database_engine()
        with Session(engine) as session:
            groups = create_groups()
            all_courses = create_courses()
            students = create_students()

            session.add_all(groups)
            session.add_all(all_courses)
            session.add_all(students)

            for student in students:
                num_courses = random.randint(1, 3)
                group = random.choice(groups)
                selected_courses = random.sample(all_courses, num_courses)
                student.group = group
                session.flush()

                for course in selected_courses:
                    student_course = StudentCourse(student_id=student.id, course_id=course.id)
                    session.add(student_course)

            session.commit()
    except Exception as error:
        raise Exception(f"Error: {error}")


if __name__ == "__main__":
    test()
