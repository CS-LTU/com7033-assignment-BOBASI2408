from flask import Blueprint, jsonify, request
from ..models import Patient
from .. import db

patient_blueprint = Blueprint('patient_blueprint', __name__)

@patient_blueprint.route('/patients', methods=['GET'])
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@patient_blueprint.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient is None:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient.to_dict())

@patient_blueprint.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    patient = Patient(
        name=data['name'],
        email=data['email'],
        age=data['age'],
        hypertension=data['hypertension'],
        heart_disease=data['heart_disease'],
        ever_married=data['ever_married'],
        work_type=data['work_type'],
        residence_type=data['residence_type'],
        avg_glucose_level=data['avg_glucose_level'],
        bmi=data['bmi'],
        smoking_status=data['smoking_status'],
        stroke=data['stroke']
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201

@patient_blueprint.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient is None:
        return jsonify({'error': 'Patient not found'}), 404
    data = request.get_json()
    patient.name = data['name']
    patient.email = data['email']
    patient.age = data['age']
    patient.hypertension = data['hypertension']
    patient.heart_disease = data['heart_disease']
    patient.ever_married = data['ever_married']
    patient.work_type = data['work_type']
    patient.residence_type = data['residence_type']
    patient.avg_glucose_level = data['avg_glucose_level']
    patient.bmi = data['bmi']
    patient.smoking_status = data['smoking_status']
    patient.stroke = data['stroke']
    db.session.commit()
    return jsonify(patient.to_dict())

@patient_blueprint.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient is None:
        return jsonify({'error': 'Patient not found'}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted'})
