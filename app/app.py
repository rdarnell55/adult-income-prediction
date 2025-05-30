# =============================================================================
# Flask Web App to Deploy ML Model - Adult Income Prediction
# -----------------------------------------------------------------------------
# This Flask app loads a trained Logistic Regression model and scaler
# to predict whether a user earns more than $50K/year based on input features.
#
# It exposes a simple web interface for input and displays the prediction.
# =============================================================================

import os
import joblib
import pandas as pd
from flask import Flask, request, render_template

# Set base directory to ensure consistent file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Create Flask App Instance ---
app = Flask(__name__)

# Load the trained machine learning model, scaler, and label encoders
MODEL_PATH = os.path.join(BASE_DIR, "../model/model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "../model/preprocess.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "../model/label_encoders.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoders = joblib.load(ENCODERS_PATH)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html') # Simple HTML form to collect user input

# Define the route for prediction handling
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Debug: Show what form fields are coming in
        print("Form Data:", request.form)

        # Get all form data safely
        age = int(request.form.get('age', 0))
        workclass = request.form.get('workclass', 'Private')
        education = request.form.get('education', 'HS-grad')
        marital_status = request.form.get('marital_status', 'Never-married')
        occupation = request.form.get('occupation', 'Sales')
        relationship = request.form.get('relationship', 'Not-in-family')
        race = request.form.get('race', 'White')
        sex = request.form.get('sex', 'Male')
        capital_gain = int(request.form.get('capital_gain', 0))
        capital_loss = int(request.form.get('capital_loss', 0))
        hours_per_week = int(request.form.get('hours_per_week', 40))
        native_country = request.form.get('native_country', 'United-States')

        # Organize inputs into a DataFrame
        input_data = pd.DataFrame([[
            age, workclass, education, marital_status, occupation,
            relationship, race, sex, capital_gain, capital_loss,
            hours_per_week, native_country
        ]], columns=[
            'age', 'workclass', 'education', 'marital-status', 'occupation',
            'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
            'hours-per-week', 'native-country'
        ])

        # Apply label encoding for categorical columns
        for column in input_data.columns:
            if column in label_encoders:
                le = label_encoders[column]
                input_data[column] = le.transform(input_data[column])

        # Apply scaling
        input_scaled = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_scaled)
        result = '>50K' if prediction[0] == 1 else '<=50K'

        return render_template('index.html', prediction_text=f'Predicted Income: {result}')

    except Exception as e:
        print("Prediction error:", e)
        return render_template('index.html', prediction_text=f'Error: {e}')

# Run the Flask application
if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port)