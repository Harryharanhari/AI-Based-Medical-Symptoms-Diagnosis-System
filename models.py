from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='patient') # admin, doctor, patient
    
    diagnoses = db.relationship('Diagnosis', backref='patient', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', foreign_keys='Appointment.patient_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    symptoms_json = db.Column(db.Text) # Stored as JSON string
    risk_score = db.Column(db.Integer)
    prediction_results_json = db.Column(db.Text) # Top 3 diseases as JSON
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_symptoms(self, symptoms_dict):
        self.symptoms_json = json.dumps(symptoms_dict)

    def get_symptoms(self):
        return json.loads(self.symptoms_json) if self.symptoms_json else {}

    def set_predictions(self, predictions_list):
        self.prediction_results_json = json.dumps(predictions_list)

    def get_predictions(self):
        return json.loads(self.prediction_results_json) if self.prediction_results_json else []

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    available_days = db.Column(db.String(200)) # e.g., "Mon,Tue,Wed"
    bio = db.Column(db.Text)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date)
    time_slot = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, Completed, Cancelled
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
