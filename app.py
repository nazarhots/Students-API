from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

from utils.db_utils import create_database_engine
from models import Student
from logger.logger import create_logger
from utils.validation import validate_empty_values


app = Flask(__name__)
api = Api(app)
Session = sessionmaker(bind=create_database_engine())
session = Session()
logger = create_logger()

STUDENTS_PER_PAGE = 10

error_msg = "An unexpected error has occurred, and our team is currently investigating the issue."

class StudentsListResource(Resource):
    """Resource for retrieving a list of students or creating a new student. """
    
    def get(self):
        page = request.args.get("page", default=1)
        per_page = request.args.get("per_page", default=STUDENTS_PER_PAGE)
        try:
            query = session.query(Student)
            pagination = paginate(query, page, per_page)
            result = [student.to_dict() for student in pagination.items]
            return result
        except Exception as error:
            logger.error(str(error))
            return error_msg, 500
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("group_id", type=int, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()
        
        group_id = args["group_id"]
        first_name = args["first_name"]
        last_name = args["last_name"]
        
        validation_result = validate_empty_values(group_id, first_name, last_name)
        if validation_result:
            logger.info(
                f"Client sent bad args, group_id - {group_id}, first_name - {first_name}, last_name - {last_name}")
            return validation_result
        
        try:
            new_student = Student(group_id=group_id,
                                    first_name=first_name,
                                    last_name=last_name)
            session.add(new_student)
            session.commit()
            return f"Student {args['first_name']} created successfully"
        except Exception as error:
            session.rollback()
            logger.error(str(error))
            return error_msg, 500



class StudentResource(Resource):
    """Resource for updating and deleting student information. """
    
    def put(self, student_id: int):
        parser = reqparse.RequestParser()
        parser.add_argument("group_id", type=int, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()
        
        group_id = args["group_id"]
        first_name = args["first_name"]
        last_name = args["last_name"]
        
        validation_result = validate_empty_values(group_id, first_name, last_name)
        if validation_result:
            logger.info(
                f"Client sent bad args, group_id - {group_id}, first_name - {first_name}, last_name - {last_name}")
            return validation_result
        try:
            student = session.query(Student).get(student_id)
            
            if not student:
                return f"Student with ID {student_id} not found"
            
            student.group_id = group_id
            student.first_name = first_name
            student.last_name = last_name
            session.commit()
            return f"Student with ID {student_id} updated successfully"
        except Exception as error:
            session.rollback()
            logger.error(str(error))
            return error_msg, 500

        
    def delete(self, student_id: int):
        try:
            student = session.query(Student).get(student_id)
            if not student:
                return f"Student with ID {student_id} not found"
            session.delete(student)
            session.commit()
            return f"Student with ID {student_id} deleted successfully"
        except Exception as error:
            session.rollback()
            logger.error(str(error))
            return error_msg, 500


api.add_resource(StudentsListResource, "/api/v1/students")
api.add_resource(StudentResource, "/api/v1/students/<int:student_id>")


if __name__ == "__main__":
    app.run(debug=True)