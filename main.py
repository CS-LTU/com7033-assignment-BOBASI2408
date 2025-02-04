from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from utils.encryption import encrypt, decrypt
from utils.validation import validate_patient_data, validate_user_data
from utils.send_email import send_medical_record
from utils.predict import predict_stroke
from utils.ai import chatbot_response
from app.models import Patient, User
from sqlalchemy.exc import IntegrityError
from config import Config, DevelopmentConfig, config
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
import csv
from extensions import db
data_record={} 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(config_object=None):
    file_path = os.path.abspath(os.getcwd()) + "/database/sqlite/patient.db"

    app = Flask(__name__)
    app.secrete_key = "12345678910"

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object('config.DevelopmentConfig')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    mongo_client = MongoClient(app.config['MONGO_URI'])  # Use MONGO_URI from config
    mongo_db = mongo_client["patients_db"]  # Access the database named "patients_db"
    mongo_patients_collection = mongo_db["patients"]  # Access the "patients" collection

    # Store MongoDB objects in the app for reuse
    app.mongo_db = mongo_db
    app.mongo_patients_collection = mongo_patients_collection


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
            stroke=predict_stroke(data))
        data_record.update(patient.to_dict())
        
        try:        
            db.session.add(patient)
            db.session.commit()
            result = 'You might have Stroke.'if patient.stroke == True else 'No sign of Stroke detected.'
            send_medical_record(data=patient.to_dict())
            # print(patient.to_dict())
            return render_template('result.html', result=result)
        except IntegrityError as e:
            flash('Each entry must have a Unique email.',"danger")
            return redirect(url_for('create_patient'))
        

    @app.route('/chatbot', methods=['GET'])
    def chatbot():
        return render_template('chat.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        """
        Endpoint for chatbot communication.
        Expects a JSON payload with a 'text' field containing the user's message.
        """
        user_message = request.json.get('text', '')
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Replace this with your AI logic
        print(data_record)
        response = chatbot_response([user_message, data_record])

        return jsonify({'response': response})
           
        
    
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
                # db.session.rollback()
                flash('Account with UserName or Email Exist. Please Login', 'error')
                # print(str(e))  # For debugging
                return redirect(url_for('register'))
        return render_template('register.html')
    
    
    @app.route('/manage_patients', methods=['GET', 'POST'])
    def manage_patients():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash("No file part in request", "danger")
                return redirect(url_for('manage_patients'))
            
            file = request.files['file']

            if file.filename == '':
                flash("No selected file", "danger")
                return redirect(url_for('manage_patients'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', filename)
                file.save(file_path)

                # Process CSV and insert data into MongoDB
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    patients = []
                    for row in csv_reader:
                        try:
                            row['age'] = int(row.get('age', 0))
                            row['avg_glucose_level'] = float(row.get('avg_glucose_level', 0))
                            row['bmi'] = float(row.get('bmi', 0))
                            row['hypertension'] = row.get('hypertension', '').lower() == 'true'
                            row['heart_disease'] = row.get('heart_disease', '').lower() == 'true'
                            row['ever_married'] = row.get('ever_married', '').lower() == 'true'
                            row['work_type'] = row.get('work_type', '').lower() == 'true'
                            row['residence_type'] = row.get('residence_type', '').lower() == 'true'
                            row['smoking_status'] = row.get('smoking status', '').lower() == 'true'
                            row['stroke'] = int(row.get('stroke', 0))
                            patients.append(row)
                        except ValueError:
                            flash(f"Invalid data format in row: {row}", "warning")

                    if patients:
                        mongo_patients_collection.insert_many(patients)
                        flash("Patients uploaded successfully!", "success")
                    else:
                        flash("No valid data to upload.", "danger")

                os.remove(file_path)  # Clean up uploaded file
                return redirect(url_for('manage_patients'))

        # Fetch all patients from MongoDB
        patients = list(mongo_patients_collection.find({}, {"_id": 0}))
        return render_template('manage_patients.html', patients=patients)

    @app.route('/delete_patient/<id>', methods=['POST'])
    def delete_patient(id):
        mongo_patients_collection.delete_one({"id": id})
        # flash("Patient deleted successfully!", "success")
        return redirect(url_for('manage_patients'))
    return app

if __name__ == '__main__':
    app = create_app()  # Call create_app() to get the app instance

    # Ensure tables are created when running the app
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist already

    app.run(debug=True)