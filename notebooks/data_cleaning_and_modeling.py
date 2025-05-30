#!/usr/bin/env python
# coding: utf-8

# In[3]:


# =============================================================================
# Adult Income Prediction - Data Cleaning and Model Training
# -----------------------------------------------------------------------------
# This notebook demonstrates how to load the Adult Income dataset from UCI,
# preprocess it, train a logistic regression model, and save the model and
# preprocessing pipeline for later deployment using Flask.
#
# Dataset Source:
# https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
#
# The goal is to predict whether an individual earns more than $50K/year
# based on demographic and employment data.
# =============================================================================

# --- Import required libraries ---
import pandas as pd                  # For data manipulation
import numpy as np                   # For numerical operations
from sklearn.model_selection import train_test_split  # To split the dataset
from sklearn.preprocessing import LabelEncoder, StandardScaler  # For encoding and scaling
from sklearn.linear_model import LogisticRegression    # ML model
from sklearn.metrics import classification_report      # Model evaluation
import joblib                        # For saving model and preprocessing pipeline

# --- Load the dataset from UCI repository ---
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

# List of column names based on the dataset documentation
column_names = [
    "age", "workclass", "fnlwgt", "education", "education-num", 
    "marital-status", "occupation", "relationship", "race", 
    "sex", "capital-gain", "capital-loss", "hours-per-week", 
    "native-country", "income"
]

# Load the dataset with column names and handle missing values
# " ?" is used in the dataset to represent missing data
df = pd.read_csv(url, names=column_names, na_values=" ?", skipinitialspace=True)

# Display the shape and the first few rows of the dataset
print("Dataset Shape:", df.shape)
print(df.head())

# --- Drop rows with missing values ---
# Note: You can also use imputation instead of dropping, but this is simpler for now
df.dropna(inplace=True)
print("After dropping missing values:", df.shape)

# --- Encode categorical variables using Label Encoding ---
# This converts string labels into numeric values
categorical_cols = df.select_dtypes(include=['object']).columns

label_encoders = {}  # To save encoders for each column (used later in deployment)

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# --- Separate features (X) and target label (y) ---
X = df.drop(["income", "fnlwgt"], axis=1)  # All columns except 'income' and 'fnlwgt'
y = df["income"]               # Target variable (0 or 1)

# --- Feature Scaling ---
# Standardize features to have zero mean and unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Split the dataset into training and testing sets ---
# 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42)

# --- Train the Model ---
# Using Logistic Regression for binary classification
model = LogisticRegression()
model.fit(X_train, y_train)

# --- Model Evaluation ---
# Predict on test data and print classification report
y_pred = model.predict(X_test)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# --- Save the Trained Model and Scaler for Deployment ---
# These will be used later in the Flask app to make live predictions

# Save model
joblib.dump(model, "../model/model.pkl")

# Save scaler
joblib.dump(scaler, "../model/preprocess.pkl")

# Note: If needed, you could also save the label_encoders dictionary
# using joblib or pickle for full reproducibility.


# In[ ]:




