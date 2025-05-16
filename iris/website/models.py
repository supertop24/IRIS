from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    school_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    phone_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255))
    dob = db.Column(db.DateTime, nullable=False)
    profile = db.Column(db.LargeBinary, nullable=True)
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

class student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, nullable=False)

class teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    main_class = db.Column(db.Integer, nullable=False)
    sub_class = db.Column(db.Integer, nullable=True)
    subject = db.Column(db.String(1))

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
    target = db.Column(db.String(1))
    target_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

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