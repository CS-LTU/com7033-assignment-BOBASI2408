Stroke_Prediction_Dataset/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── patient_routes.py
│   │   └── user_routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── patient.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
├── requirements.txt
├── README.md
├── .gitignore
├── config.json
├── database/
│   ├── sqlite/
│   │   ├── patient.db
│   │   └── user.db
│   └── mongodb/
│       ├── patient_collection/
│       └── user_collection/
├── tests/
│   ├── __init__.py
│   ├── test_patient_routes.py
│   ├── test_user_routes.py
│   ├── test_models.py
│   └── test_database.py
├── utils/
│   ├── __init__.py
│   ├── encryption.py
│   └── validation.py
├── .git/
├── .github/
├── .gitattributes
├── LICENSE
├── app.py
├── config.py
├── manage.py
├── requirements.txt
├── run.py
└── venv/


### Developer Assignment Brief  

#### **Overview**
According to the World Health Organization (WHO), stroke ranks as the second leading cause of death globally. For this assignment, you will build a secure web application for a local hospital to manage a **Stroke Prediction Dataset**. The application will enable doctors to handle patient data—including registration, medical history, and lifestyle factors—to predict the likelihood of a stroke.  

---

### **Dataset**  
The dataset for this assignment is available on Kaggle: [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/data). It includes the following attributes:  
- **id**: Unique identifier  
- **gender**: `"Male"`, `"Female"`, or `"Other"`  
- **age**: Patient's age  
- **hypertension**: `0` (no hypertension), `1` (has hypertension)  
- **ever_married**: `"No"` or `"Yes"`  
- **work_type**: `"Children"`, `"Govt_job"`, `"Never_worked"`, `"Private"`, or `"Self-employed"`  
- **Residence_type**: `"Rural"` or `"Urban"`  
- **avg_glucose_level**: Average glucose level in blood  
- **bmi**: Body Mass Index  
- **smoking_status**: `"Formerly smoked"`, `"Never smoked"`, `"Smokes"`, or `"Unknown"` (unavailable information)  
- **stroke**: `1` (patient had a stroke), `0` (patient did not have a stroke)  

---

### **Key Objectives**
Upon completion, you should demonstrate:  
1. An understanding of secure programming concepts and techniques.  
2. Proficiency in data manipulation and analysis using popular frameworks.  
3. A professional approach to ethical and secure software development.  
4. The ability to design technical solutions for complex problems.  

---

### **Tasks**
#### **1. Web Application Development**  
Create a secure web application using **Python Flask** to manage the Stroke Prediction Dataset. The application should:  
- Include a fully functional web server with a **user-friendly interface**.  
- Support single or multiple databases (SQLite and MongoDB) for **secure data storage** and retrieval.  
- Implement secure programming techniques, such as:  
  - **Encryption** for patient registration data.  
  - **Input validation** to ensure data integrity and prevent vulnerabilities.  

#### **2. Secure Development Techniques**  
Show proficiency in secure system design, including:  
- **Encryption**: Use methods like password hashing.  
- **Input Validation**: Prevent injection attacks and other vulnerabilities.  
- **Database Management**: Use SQLite for user data (e.g., registration) and MongoDB for medical records.  
- **Unit Testing**: Ensure system functionality and reliability.  
- **Version Control**: Use GitHub to track project progress, with meaningful commit messages.  

---

### **Submission Details**
- **Release Date**: 15 October 2024  
- **Deadline**: 29 November 2024, midday. Late submissions may affect your grade.  
- **Deliverables**:  
  1. Upload your project to the GitHub repository provided in the module’s GitHub Classroom:  
     `https://github.com/CS-LTU/com7033-assignment-XXXX`  
     Replace `XXXX` with your GitHub username.  
  2. Submit via Moodle before the deadline.  

**Note**: Late submissions require notifying the assessment team and module leader before the due time.  

---

### **Marking Criteria**
#### **Pass (50%)**
- Basic web app with a functional UI.  
- Single database (SQLite or MongoDB).  
- At least one security feature (e.g., password encryption or input validation).  
- GitHub usage with at least one commit.  

#### **Merit (60%)**  
- Fully functional web app with an advanced interface.  
- Multiple databases for managing different data categories.  
- Ability to add, update, and delete records.  
- Two security features (e.g., input validation and password hashing).  
- At least four GitHub commits with meaningful messages.  
- Partial code documentation.  
- One unit test.  

#### **Distinction (70%)**  
- Professional, customized UI.  
- Interconnected databases for enhanced data security and query efficiency.  
- Three or more secure development techniques.  
- Eight or more GitHub commits with detailed messages.  
- Multiple tests across features.  
- Fully documented code.  

#### **Exceptional Distinction (80%)**  
- Highly efficient, scalable code.  
- Use of third-party APIs or libraries for additional security.  
- Comprehensive documentation (installation, usage, and API references).  
- Extensive testing (unit, integration, and end-to-end tests).  
- Robust GitHub practices with detailed commit history, branches, and pull requests.  

---

### **Support and Resources**
- Use the module handbook and School of Computer Science Teams community for guidance.  
- Contact support via Microsoft Teams or email during working hours.  
- Access Student Support services for assistance with academic or personal matters via the LTU app.  

---


Prepare to demonstrate your work following submission if required.#   c o m 7 0 3 3 - a s s i g n m e n t - B O B A S I 2 4 0 8  
 