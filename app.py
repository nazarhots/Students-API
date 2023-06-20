from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

from utils.db_utils import create_database_engine
from models import Student, StudentCourse
from logger.logger import create_logger
from utils.validation import validate_values
from utils.decorators import retry_app_db_operation


app = Flask(__name__)
api = Api(app)
Session = sessionmaker(bind=create_database_engine())
session = Session()
logger = create_logger()

STUDENTS_PER_PAGE = 10


class StudentsListResource(Resource):
    """Resource for retrieving a list of students or creating a new student. """

    @retry_app_db_operation
    def get(self):
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=STUDENTS_PER_PAGE, type=int)
        
        query = session.query(Student)
        pagination = paginate(query, page, per_page)
        result = [student.to_dict() for student in pagination.items]
        return result

    @retry_app_db_operation
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("group_id", type=int, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()

        group_id = args["group_id"]
        first_name = args["first_name"]
        last_name = args["last_name"]

        validation_result = validate_values(group_id, first_name, last_name)
        if validation_result:
            return validation_result

        new_student = Student(
            group_id=group_id,
            first_name=first_name,
            last_name=last_name
        )
        session.add(new_student)
        session.commit()
        msg = f"Student {args['first_name']} created successfully"
        logger.debug(msg)
        return msg, 201


class StudentResource(Resource):
    """Resource for updating and deleting student information. """

    @retry_app_db_operation
    def put(self, student_id: int):
        parser = reqparse.RequestParser()
        parser.add_argument("group_id", type=int, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()

        group_id = args["group_id"]
        first_name = args["first_name"]
        last_name = args["last_name"]

        validation_result = validate_values(group_id, first_name, last_name)
        if validation_result:
            return validation_result

        student = session.query(Student).get(student_id)
        if not student:
            msg = f"Student with ID {student_id} not found"
            logger.debug(msg)
            return msg, 404

        student.group_id = group_id
        student.first_name = first_name
        student.last_name = last_name
        session.commit()
        msg = f"Student with ID {student_id} updated successfully"
        logger.debug(msg)
        return msg, 201

    @retry_app_db_operation
    def delete(self, student_id: int):
        student = session.query(Student).get(student_id)
        if not student:
            msg = f"Student with ID {student_id} not found"
            logger.debug(msg)
            return msg, 404

        session.query(StudentCourse).filter_by(student_id=student_id).delete()
        session.delete(student)
        session.commit()
        return f"Student with ID {student_id} deleted successfully"


api.add_resource(StudentsListResource, "/api/v1/students")
api.add_resource(StudentResource, "/api/v1/students/<int:student_id>")
