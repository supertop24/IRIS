from . import db
from datetime import datetime
from flask_login import UserMixin
import enum
from sqlalchemy import Enum

class TeacherRole(enum.Enum):
    MAIN = "main"
    SUB = "sub"
    ASSISTANT = "assistant"

class TeacherClassAssociation(db.Model):
    __tablename__ = 'teacher_class_association'
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    role = db.Column(Enum(TeacherRole), nullable=False)

    teacher = db.relationship("Teacher", back_populates="class_associations")
    class_ = db.relationship("Class", back_populates="teacher_associations")

student_classes = db.Table(
    'student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
)

teacher_classes = db.Table(
    'teacher_classes',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    school_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    phone_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255))
    dob = db.Column(db.DateTime, nullable=True)
    profile = db.Column(db.LargeBinary, nullable=True)
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(1))     
    code = db.Column(db.String(10), nullable=False)

    teachers = db.relationship('Teacher', secondary=teacher_classes, back_populates='classes')

    students = db.relationship('User', secondary=student_classes, back_populates='enrolled_classes')

    assessments = db.relationship('Assessment', backref='class_', lazy=True)

class student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    enrolled_classes = db.relationship('Classes', secondary=student_classes, back_populates='students')

class teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    classes = db.relationship('Class', secondary=teacher_classes, back_populates='teachers')


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_code = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    # status = db.Column (enum for options - insert later)

    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    # assessments must be uploaded as files - single pdf, including isntructions and criteria, then separate file just for teachers - including resources and other marking notes
    # a new class/table for "submissions" needed for tracking. Must contain a relationship to the assessment, the class, the students and the status



class caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(1))
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(1))
    phone_number = db.Column(db.Integer, nullable=True)
    home_number = db.Column(db.Integer, nullable=True)
    work_number = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255))
    dob = db.Column(db.DateTime, nullable=False)
    relationship = db.Column(db.String(1))

class class_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1))
    target = db.Column(db.String(1))
    target_id = db.Column(db.Integer, nullable=False)
    value= db.Column(db.Boolean, default=False)
    note=db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 

class message_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(1))
    sender_id = db.Column(db.Integer, nullable=False)
    target = db.Column(db.String(1))
    target_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class extracurricular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turor_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(10))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class extracurricular_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    ex_id = db.Column(db.Integer, nullable=False)
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(1), nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #default=db.func.current_timestamp())

class pastoral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(1))
    target = db.Column(db.String(1))
    target_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(1))
    grade = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    file = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())