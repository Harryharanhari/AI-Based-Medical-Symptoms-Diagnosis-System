def get_symptom_weights():
    # Base weights for symptoms (1-10)
    return {
        'itching': 1, 'skin_rash': 3, 'nodal_skin_eruptions': 4, 'continuous_sneezing': 2, 'shivering': 4,
        'chills': 3, 'joint_pain': 3, 'stomach_pain': 5, 'acidity': 3, 'ulcers_on_tongue': 4, 'muscle_wasting': 7,
        'vomiting': 5, 'burning_micturition': 6, 'spotting_urination': 6, 'fatigue': 4, 'weight_gain': 4,
        'anxiety': 5, 'cold_hands_and_feets': 5, 'mood_swings': 5, 'weight_loss': 6, 'restlessness': 5,
        'lethargy': 4, 'patches_in_throat': 6, 'irregular_sugar_level': 8, 'cough': 4, 'high_fever': 7,
        'sunken_eyes': 5, 'breathlessness': 9, 'sweating': 3, 'dehydration': 8, 'indigestion': 4,
        'headache': 3, 'yellowish_skin': 7, 'dark_urine': 7, 'nausea': 5, 'loss_of_appetite': 5,
        'pain_behind_the_eyes': 4, 'back_pain': 3, 'constipation': 4, 'abdominal_pain': 5, 'diarrhoea': 6,
        'mild_fever': 5, 'yellow_urine': 5, 'yellowing_of_eyes': 7, 'acute_liver_failure': 10,
        'fluid_overload': 8, 'swelling_of_stomach': 7, 'swelled_lymph_nodes': 6, 'malaise': 5, 'blurred_and_distorted_vision': 8,
        'chest_pain': 10, 'dizziness': 6, 'red_spots_over_body': 4, 'muscle_pain': 5, 'stiff_neck': 7
    }

def calculate_risk_score(selected_symptoms_with_severity):
    """
    selected_symptoms_with_severity: dict {symptom_name: severity_1_to_5}
    Formula: Risk Score = Σ (Presence(1) × Severity(1-5) × Weight(1-10))
    """
    weights = get_symptom_weights()
    total_score = 0
    max_possible_per_symptom = 50 # Max severity (5) * Max weight (10)
    
    for symptom, severity in selected_symptoms_with_severity.items():
        weight = weights.get(symptom, 5) # Default weight 5 if not found
        total_score += (severity * weight)
        
    # Scale score to a 0-100 range for visualization (assuming a typical max score of 200 based on ~4-5 high severity symptoms)
    scaled_score = (total_score / 200) * 100
    return min(100, round(scaled_score))

def get_risk_classification(score):
    if score <= 25:
        return {'label': 'Low', 'color': 'green', 'description': 'Minor symptoms. Monitor and rest.'}
    elif score <= 50:
        return {'label': 'Medium', 'color': 'orange', 'description': 'Moderate risk. Please consult a doctor soon.'}
    else:
        return {'label': 'High', 'color': 'red', 'description': 'Critical condition detected! Seek medical attention immediately.'}
