import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import json
import os

# Load the trained model
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_name = os.path.join(base_dir, 'utils', 'model.h5')
model = tf.keras.models.load_model(model_name)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress INFO and WARNING messages


# Preprocessing function
def preprocess_input(data):
    """
    Preprocess the input JSON data to match the training features.
    """
    # Extract relevant features
    features = {
        "id": data.get("age"),
        "hypertension": data.get("hypertension"),
        "heart_disease": data.get("heart_disease"),
        "avg_glucose_level": data.get("avg_glucose_level"),
        "bmi": data.get("bmi"),
    }
    
    # Map categorical features using one-hot encoding (if used during training)
    # work_type_map = {"Private": 0, "Self-employed": 1, "Govt_job": 2, "children": 3, "Never_worked": 4}
    # smoking_status_map = {"never smoked": 0, "formerly smoked": 1, "smokes": 2, "Unknown": 3}
    
    # features["work_type"] = work_type_map.get(features["work_type"], 4)  # Default to "Never_worked" if missing
    # features["smoking_status"] = smoking_status_map.get(features["smoking_status"], 3)  # Default to "Unknown" if missing
    
    # Convert features into a NumPy array
    input_data = np.array([
        features["id"],
        features["hypertension"],
        features["heart_disease"],
        features["avg_glucose_level"],
        features["bmi"],
    ]).reshape(1, -1)
    
    return input_data

# Prediction function
def predict_stroke(data):
    """
    Predict if the patient is at risk of stroke based on their data.
    
    Args:
        data (dict): Patient data in JSON format.
        
    Returns:
        bool: True if the patient is at risk of stroke, False otherwise.
    """
    # Preprocess the input data
    input_data = preprocess_input(data)
    
    # Standardize the features (Ensure to use the same scaler as during training)
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_data_scaled)
    
    # Interpret the result (1 = Stroke, 0 = No Stroke)
    return prediction[0][0] > 0.5  # Returns True if prediction > 0.5, else False

