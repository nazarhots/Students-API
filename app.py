from flask import Flask, jsonify, request
from flask_restful import Api
from sqlalchemy_pagination import paginate
from sqlalchemy.orm import sessionmaker

from db_utils import create_database_engine
from models import Student


app = Flask(__name__)
api = Api(app)
Session = sessionmaker(bind=create_database_engine())
session = Session()

STUDENTS_PER_PAGE = 10


@app.route("/api/v1/students", methods=["GET"])
def get_all_students():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=STUDENTS_PER_PAGE, type=int)
    try:
        query = session.query(Student)
        pagination = paginate(query, page, per_page)
        result = [student.to_dict() for student in pagination.items]
        return jsonify(result)
    except Exception as error:
        return jsonify({"Error": str(error)}), 500


@app.route("/api/v1/students", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        new_student = Student(group_id=data["group_id"],
                                first_name=data["first_name"],
                                last_name=data["last_name"])
        session.add(new_student)
        session.commit()
        return f"Student {data['first_name']} created successfully"
    except Exception as error:
        session.rollback()
        return jsonify({"Error": str(error)}), 500
    finally:
        session.close()


@app.route("/api/v1/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        student = session.query(Student).get(student_id)
        
        if not student:
            return f"Student with ID {student_id} not found"
        
        data = request.get_json()
        student.group_id = data["group_id"]
        student.first_name = data["first_name"]
        student.last_name = data["last_name"]
        session.commit()
        return f"Student with ID {student_id} updated successfully"
    except Exception as error:
        session.rollback()
        return jsonify({"Error": str(error)}), 500
    finally:
        session.close()


@app.route("/api/v1/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        student = session.query(Student).get(student_id)
        if not student:
            return f"Student with ID {student_id} not found"
        session.delete(student)
        session.commit()
        return f"Student with ID {student_id} deleted successfully"
    except Exception as error:
        session.rollback()
        return jsonify({"Error": str(error)}), 500
    finally:
        session.close()
