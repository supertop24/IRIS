from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(255))
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())
