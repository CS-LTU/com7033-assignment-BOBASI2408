from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hypertension = db.Column(db.Boolean, nullable=False)
    heart_disease = db.Column(db.Boolean, nullable=False)
    ever_married = db.Column(db.Boolean, nullable=False)
    work_type = db.Column(db.String(100), nullable=False)
    residence_type = db.Column(db.String(100), nullable=False)
    avg_glucose_level = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    smoking_status = db.Column(db.String(100), nullable=False)
    stroke = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, email, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke):
        self.name = name
        self.email = email
        self.age = age
        self.hypertension = hypertension
        self.heart_disease = heart_disease
        self.ever_married = ever_married
        self.work_type = work_type
        self.residence_type = residence_type
        self.avg_glucose_level = avg_glucose_level
        self.bmi = bmi
        self.smoking_status = smoking_status
        self.stroke = stroke

    def __repr__(self):
        return f"Patient('{self.name}', '{self.email}', '{self.age}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'hypertension': self.hypertension,
            'heart_disease': self.heart_disease,
            'ever_married': self.ever_married,
            'work_type': self.work_type,
            'residence_type': self.residence_type,
            'avg_glucose_level': self.avg_glucose_level,
            'bmi': self.bmi,
            'smoking_status': self.smoking_status,
            'stroke': self.stroke,
            'created_at': self.created_at
        }
