from . import db
from datetime import datetime, timedelta, date
from flask_login import UserMixin
import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

# The following three tables are used to connect the Student and Teacher models with the Class model.  

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

class StudentClassAssociation(db.Model):
    __tablename__ = 'student_class_association'
    
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)

    student = db.relationship('Student', back_populates='enrolled_classes')
    class_ = db.relationship('Class', back_populates='student_associations')

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50))
    gender = db.Column(db.String(15))
    phone_number = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255))
    profile = db.Column(db.LargeBinary, nullable=True)
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    enrolled_classes = db.relationship('StudentClassAssociation', back_populates='student')
    dob = db.Column(db.DateTime, nullable=True)
    personal_email = db.Column(db.String(120), unique=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = 'student'

    # MEthod to get the student's schedule for the week
    def get_weekly_schedule(self, start_date=None, end_date=None):
        if not start_date: # if a start date isn't given, then it will get today's date. Then, we're using timedelta to calculate the number of days since Monday, and declaring "end date" (Sunday) as 6 days after that (6 because Monday is indexed at 0).
            today = datetime.today()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)

        return (
            ClassSession.query
            .join(Class)
            .join(StudentClassAssociation)
            .filter(
                StudentClassAssociation.student_id == self.id,
                ClassSession.date >= start_date,
                ClassSession.date <= end_date
            )
            .order_by(ClassSession.date)
            .all()
            
        )

    #need to add get_weekly_schedule method to here and Teacher classes to render into calendar 

class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    class_associations = db.relationship("TeacherClassAssociation", back_populates="teacher")
    classes = db.relationship("Class", secondary='teacher_class_association', viewonly=True)
    dob = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = 'teacher'

    def get_daily_schedule(self, target_date: date):
        return (
            db.session.query(ClassSession)
            .join(Class)
            .join(TeacherClassAssociation)
            .join(Period, ClassSession.period_id == Period.id)
            .filter(TeacherClassAssociation.teacher_id == self.id)
            .filter(ClassSession.date == target_date)
            .order_by(Period.id)
            .all()
        )

    def get_weekly_schedule(self, start_date=None, end_date=None):
        if not start_date:
            today = datetime.today()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)

        return (
            ClassSession.query
            .join(Class)
            .join(TeacherClassAssociation)
            .filter(
                TeacherClassAssociation.teacher_id == self.id,
                ClassSession.date >= start_date,
                ClassSession.date <= end_date
            )
            .order_by(ClassSession.date)
            .all()
        )


class Class(db.Model):
    __tablename__ = 'class'    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(15))     
    code = db.Column(db.String(15), nullable=False)

    # The two teacher relationship lines serve different purposes. The first one calls the "TeacherClassAssociation" model, which holds their role info. If we just want to call teacher objects, we can use the 2nd line which gets the Teacher model directly.  
    teacher_associations = db.relationship("TeacherClassAssociation", back_populates="class_")
    teachers = db.relationship("Teacher", secondary='teacher_class_association', viewonly=True)

    student_associations = db.relationship('StudentClassAssociation', back_populates='class_')

    assessments = db.relationship('Assessment', backref='class_', lazy=True)

    schedule = db.Column(db.String, nullable=True)
    sessions = db.relationship('ClassSession', backref='class_', cascade="all, delete-orphan")

class ClassSession(db.Model):
    __tablename__ = 'class_session'   
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)

    period = db.relationship('Period')

class Period(db.Model):
    __tablename__ = 'period'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False) 
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


class AttendanceStatus(enum.Enum):
    Present = "present"
    AbsentUnjustified = "absentunjustified"
    AbsentJustified = "absentjustified"
    Late = "late"
 
class Attendance(db.Model):
    __tablename__ = 'attendance'  
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('class_session.id'), primary_key=True)
    status = db.Column(Enum(AttendanceStatus), nullable=False) 
    note = db.Column(db.String(50), nullable=True)

    student = db.relationship("Student", backref="attendance_records")
    session = db.relationship("ClassSession", backref="attendance_records")


class Assessment(db.Model):
    __tablename__ = 'assessment'
    id = db.Column(db.Integer, primary_key=True)
    assessment_code = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    # status = db.Column (enum for options - insert later)

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    # assessments must be uploaded as files - single pdf, including isntructions and criteria, then separate file just for teachers - including resources and other marking notes
    # a new class/table for "submissions" needed for tracking. Must contain a relationship to the assessment, the class, the students and the status

class Caregiver(db.Model):
    __tablename__ = 'caregiver'
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
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #default=db.func.current_timestamp())

class Pastoral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(1), nullable=True)
    studentID = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(50), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(50), nullable=True)
    time = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(50), nullable=True)
    studentsInvolved = db.Column(db.String(255), nullable=True)
    staffInvolved = db.Column(db.String(255), nullable=True)

class report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(1))
    grade = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    file = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())