# AI-Based-Medical-Symptoms-Diagnosis-System

A production-ready Enterprise AI Healthcare Platform built with Flask, Scikit-learn, and Grok AI.

## 🔷 Core Features
- **Symptom Analysis**: Predicts diseases using a Random Forest Classifier.
- **Risk Scoring**: Severity-weighted risk engine (0-100%).
- **Similarity Clustering**: Grouping related conditions using KMeans.
- **Admin Analytics**: Real-time clinical trends with Chart.js.
- **AI Chatbot**: Integrated Grok API for medical assistance.
- **PDF Reports**: Professional medical report generation.
- **Appointment System**: Doctor consultation booking.

## 🔷 Tech Stack
- **Backend**: Python 3.11+, Flask (App Factory), SQLAlchemy, Scikit-learn, Joblib.
- **Frontend**: HTML5, CSS3 (Dark Medical Theme), Bootstrap 5, Chart.js.
- **Deployment**: Gunicorn, PostgreSQL/SQLite compat.

## 🔷 Local Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd AI-Medical-Diagnosis-Assistant-System
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key
   GROK_API_KEY=your-xai-key
   ```

5. **Initialize Database & Seed Data**:
   ```bash
   python seed.py
   ```

6. **Run the Application**:
   ```bash
   python run.py
   ```

## 🔷 Deployment (Render)
1. Link your GitHub repo to Render.
2. Choose **Web Service**.
3. Runtime: **Python 3**.
4. Build Command: `pip install -r requirements.txt`.
5. Start Command: `gunicorn run:app`.
6. Add Environment Variables in Render dashboard.

## 🔷 Sample Accounts
- **Admin**: `admin` / `admin123`
- **Patient**: `patient1` / `patient123`

---
*Disclaimer: This is an AI-powered tool. Always consult a real doctor for medical emergencies.*


