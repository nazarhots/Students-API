from flask import Flask, jsonify, request
from flask_restful import Api

from sqlalchemy.orm import sessionmaker

from db_utils import create_database_engine
from models import Student


app = Flask(__name__)
api = Api(app)
Session = sessionmaker(bind=create_database_engine())
session = Session()


@app.route("/api/v1/students", methods=["GET"])
def get_all_students():
    query = session.query(Student).all()
    result = [student.to_dict() for student in query]
    return jsonify(result)


@app.route("/api/v1/students", methods=["POST"])
def create_student():
    data = request.get_json()
    new_student = Student(group_id=data["group_id"],
                          first_name=data["first_name"],
                          last_name=data["last_name"])
    session.add(new_student)
    session.commit()
    return f"Student {data['first_name']} created successfully"


@app.route("/api/v1/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    student = session.query(Student).get(student_id)
    
    if not student:
        return f"Student with ID {student_id} not found"
    
    data = request.get_json()
    student.group_id = data["group_id"]
    student.first_name = data["first_name"]
    student.last_name = data["last_name"]
    session.commit()
    return f"Student {student} updated successfully"


@app.route("/api/v1/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = session.query(Student).get(student_id)
    
    if not student:
        return f"Student with ID {student_id} not found"
    
    session.delete(student)
    session.commit()
    return f"Student {student_id} deleted successfully"


if __name__ == "__main__":
    app.run(debug=True)