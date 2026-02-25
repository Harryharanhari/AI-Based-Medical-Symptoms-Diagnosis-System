from flask import render_template, Blueprint, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.models import Diagnosis, User, Appointment
from sqlalchemy import func
from datetime import datetime, timedelta
import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))

    # Statistics for Charts
    # 1. Disease Distribution
    all_diagnoses = Diagnosis.query.all()
    disease_counts = {}
    for d in all_diagnoses:
        preds = d.get_predictions()
        if preds:
            top_disease = preds[0]['disease']
            disease_counts[top_disease] = disease_counts.get(top_disease, 0) + 1
    
    # 2. Risk Distribution
    risk_stats = {
        'Low': Diagnosis.query.filter(Diagnosis.risk_score <= 25).count(),
        'Medium': Diagnosis.query.filter((Diagnosis.risk_score > 25) & (Diagnosis.risk_score <= 50)).count(),
        'High': Diagnosis.query.filter(Diagnosis.risk_score > 50).count()
    }

    # 3. Last 7 Days Diagnosis Trend
    today = datetime.utcnow().date()
    trend_data = []
    trend_labels = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Diagnosis.query.filter(func.date(Diagnosis.timestamp) == date).count()
        trend_labels.append(date.strftime('%b %d'))
        trend_data.append(count)

    stats = {
        'total_patients': User.query.filter_by(role='patient').count(),
        'total_diagnoses': Diagnosis.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='Pending').count(),
        'disease_labels': list(disease_counts.keys()),
        'disease_values': list(disease_counts.values()),
        'risk_labels': list(risk_stats.keys()),
        'risk_values': list(risk_stats.values()),
        'trend_labels': trend_labels,
        'trend_values': trend_data
    }

    return render_template('admin/dashboard.html', stats=stats)
