import joblib
import os
from flask import current_app

def get_similar_diseases(disease_name):
    model_path = current_app.config['CLUSTER_MODEL_PATH']
    if not os.path.exists(model_path):
        return []

    similarity_data = joblib.load(model_path)
    disease_names = similarity_data['disease_names']
    cluster_labels = similarity_data['cluster_labels']

    if disease_name not in disease_names:
        return []

    # Find the cluster label for the given disease
    disease_index = disease_names.index(disease_name)
    target_cluster = cluster_labels[disease_index]

    # Find all diseases in the same cluster
    similar_diseases = [
        disease_names[i] for i, label in enumerate(cluster_labels)
        if label == target_cluster and disease_names[i] != disease_name
    ]

    return {
        'target_disease': disease_name,
        'cluster_label': int(target_cluster),
        'similar_diseases': similar_diseases
    }
