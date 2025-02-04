import re

def validate_patient_data(data):
    if not data['name']:
        return False, 'Name is required'
    if not data['age']:
        return False, 'Age is required'
    if not data['hypertension']:
        return False, 'Hypertension is required'
    if not data['heart_disease']:
        return False, 'Heart disease is required'
    if not data['ever_married']:
        return False, 'Ever married is required'
    if not data['work_type']:
        return False, 'Work type is required'
    if not data['residence_type']:
        return False, 'Residence type is required'
    if not data['avg_glucose_level']:
        return False, 'Average glucose level is required'
    if not data['bmi']:
        return False, 'BMI is required'
    if not data['smoking_status']:
        return False, 'Smoking status is required'
    return True, ''

def validate_user_data(data):
    if not data['username']:
        return False, 'Username is required'
    if not data['email']:
        return False, 'Email is required'
    if not data['password']:
        return False, 'Password is required'
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
        return False, 'Invalid email address'
    return True, ''
