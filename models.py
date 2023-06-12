from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    group = relationship("Group", backref="students")
    enrolled_courses = relationship("StudentCourse", back_populates="student")
    
    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100))

    enrolled_students = relationship("StudentCourse", back_populates="course")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class StudentCourse(Base):
    __tablename__ = "students_courses"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    student = relationship("Student", back_populates="enrolled_courses")
    course = relationship("Course", back_populates="enrolled_students")
