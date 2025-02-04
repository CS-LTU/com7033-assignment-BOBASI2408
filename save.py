from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from utils.encryption import encrypt, decrypt
from utils.validation import validate_patient_data, validate_user_data
from app.models import Patient, User
from sqlalchemy.exc import IntegrityError
from config import Config
import os

from extensions import db

def create_app(config_object=None):
    file_path = os.path.abspath(os.getcwd()) + "/database/sqlite/patient.db"

    app = Flask(__name__)
    app.secrete_key = "12345678910"

    if config_object:
        app.config.from_object(config_object)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return render_template('register.html')

    @app.route('/patients', methods=['GET'])
    def get_patients():
        return render_template("patient.html")


    @app.route('/patients', methods=['POST'])
    def create_patient():
        data = request.form
        hypertension = True if data.get('hypertension') == 'on' else False
        heart_disease = True if data.get('heart_disease') == 'on' else False
        ever_married = True if data.get('ever_married') == 'on' else False
        data = {
            "name": data.get("name"),
            "email": data.get("email"),
            "age": int(data.get("age")),
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "ever_married": ever_married,
            "work_type": data.get("work_type"),
            "residence_type": data.get("residence_type"),
            "avg_glucose_level": float(data.get("avg_glucose_level")),
            "bmi": float(data.get("bmi")),
            "smoking_status": data.get("smoking_status"),
            }
  
        patient = Patient(
            name=data['name'],
            age=data['age'],
            email=data["email"],
            hypertension=data['hypertension'],
            heart_disease=data['heart_disease'],
            ever_married=data['ever_married'],
            work_type=data['work_type'],
            residence_type=data['residence_type'],
            avg_glucose_level=data['avg_glucose_level'],
            bmi=data['bmi'],
            smoking_status=data['smoking_status'],
            stroke=True)
        try:        
            db.session.add(patient)
            db.session.commit()
            result = 'You might have Stroke.' if int(data["age"]) > 50 else 'No sign of Stroke detected.'
            return render_template('result.html', result=result)
        except IntegrityError as e:
            flash('Each entry must have a Unique email.',"danger")
            return redirect(url_for('create_patient'))
           
        
    
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_request():
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f'Welcome, {user.username}!')
            return redirect(url_for('get_patients'))
        
        flash('Invalid Credentials.', 'danger')
        return redirect(url_for('login'))
        
        
    @app.route('/view_patients', methods=['GET'])
    def view_patients():
        # Fetch all patients from the database
        patients = Patient.query.all()
        if not patients:
            flash("No Records Yet. Please Make Diagnosis.", "info")
        return render_template('view_patients.html', patients=patients)



    @app.route('/users', methods=['POST',"GET"])
    def create_user():
        if request.method=="POST":
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email', '')
            data = {
                    'username': username,
                    'password': password,
                    'email': email
                }
            try:    
                is_valid, error_message = validate_user_data(data)
                if not is_valid:
                    flash('All fields are required!')
                    return redirect(url_for('create_user'))

                user = User(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                db.session.add(user)
                db.session.commit()
                flash('Registration successful. Please log in.')
                return redirect(url_for('login'))

            except Exception as e:
                db.session.rollback()
                flash('Account with UserName or Email Exist. Please Login', 'error')
                print(str(e))  # For debugging
                return redirect(url_for('register'))
        return render_template('register.html')

    return app

if __name__ == '__main__':
    app = create_app()  # Call create_app() to get the app instance

    # Ensure tables are created when running the app
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist already

    app.run(debug=True)