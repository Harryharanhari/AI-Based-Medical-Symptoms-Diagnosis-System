from flask import render_template, Blueprint, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.models import Diagnosis, Appointment

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.index'))
    
    diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).order_by(Diagnosis.timestamp.desc()).limit(5).all()
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.timestamp.desc()).limit(5).all()
    
    return render_template('dashboard.html', title='Dashboard', diagnoses=diagnoses, appointments=appointments)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='User Profile')
