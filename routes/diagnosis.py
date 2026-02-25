from flask import render_template, redirect, url_for, flash, request, Blueprint, jsonify, current_app
from flask_login import login_required, current_user
import joblib
import pandas as pd
import numpy as np
import json
from app import db
from app.models import Diagnosis
from app.severity_engine import calculate_risk_score, get_risk_classification
from app.clustering import get_similar_diseases
from app.chatbot import get_medical_advice

bp = Blueprint('diagnosis', __name__)

@bp.route('/diagnose', methods=['GET', 'POST'])
@login_required
def diagnose():
    symptoms_list = joblib.load('models/symptoms_list.pkl')
    if request.method == 'POST':
        # Get selected symptoms and their severities from form
        selected_symptoms = {}
        for s in symptoms_list:
            if request.form.get(f"symptom_{s}"):
                severity = int(request.form.get(f"severity_{s}", 1))
                selected_symptoms[s] = severity
        
        if not selected_symptoms:
            flash('Please select at least one symptom', 'warning')
            return redirect(url_for('diagnosis.diagnose'))

        # 1. Disease Prediction (RandomForest)
        model = joblib.load(current_app.config['DISEASE_MODEL_PATH'])
        input_vector = np.zeros(len(symptoms_list))
        for i, s in enumerate(symptoms_list):
            if s in selected_symptoms:
                input_vector[i] = 1
        
        # Get top 3 predictions
        probas = model.predict_proba([input_vector])[0]
        top_indices = np.argsort(probas)[::-1][:3]
        top_diseases = [
            {'disease': model.classes_[i], 'probability': round(probas[i] * 100, 2)}
            for i in top_indices if probas[i] > 0
        ]

        # 2. Risk Scoring (Severity Engine)
        risk_score = calculate_risk_score(selected_symptoms)
        risk_level = get_risk_classification(risk_score)

        # 3. Similarity Clustering (KMeans)
        primary_disease = top_diseases[0]['disease'] if top_diseases else "Unknown"
        similar_info = get_similar_diseases(primary_disease)

        # 4. Save to Database
        diagnosis = Diagnosis(
            user_id=current_user.id,
            risk_score=risk_score
        )
        diagnosis.set_symptoms(selected_symptoms)
        diagnosis.set_predictions(top_diseases)
        db.session.add(diagnosis)
        db.session.commit()

        return render_template('diagnosis/result.html', 
                               diagnosis=diagnosis, 
                               risk_level=risk_level, 
                               similar_info=similar_info,
                               top_diseases=top_diseases)

    return render_template('diagnosis/form.html', symptoms=symptoms_list)

@bp.route('/api/chatbot', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = get_medical_advice([user_message])
    return jsonify({'response': response})

from app.utils.pdf_generator import generate_medical_report
from flask import send_file
import io

@bp.route('/download_report/<int:diagnosis_id>')
@login_required
def download_report(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    if diagnosis.user_id != current_user.id and current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    risk_level = get_risk_classification(diagnosis.risk_score)
    pdf_buffer = generate_medical_report(current_user, diagnosis, risk_level)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Medical_Report_{diagnosis.timestamp.strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )

@bp.route('/diagnosis/view/<int:diagnosis_id>')
@login_required
def view_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    if diagnosis.user_id != current_user.id and current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    risk_level = get_risk_classification(diagnosis.risk_score)
    similar_info = get_similar_diseases(diagnosis.get_predictions()[0]['disease'] if diagnosis.get_predictions() else "Unknown")
    
    return render_template('diagnosis/view.html', 
                           diagnosis=diagnosis, 
                           risk_level=risk_level, 
                           similar_info=similar_info)
