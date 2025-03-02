import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from main import create_app, db
from config import TestingConfig
from app.models.user import User
from app.models.patient import Patient

class TestModels(unittest.TestCase):
    def setUp(self):
        # Create a new Flask app with testing config
        self.app = create_app(TestingConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        # Clean up database after each test
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_user(self):
        """Test creation of a User model instance."""
        user = User(
            username='john_doe',
            email='john@example.com',
            password='securepassword'
        )
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('securepassword'))

    def test_create_patient(self):
        """Test creation of a Patient model instance."""
        patient = Patient(
            name='Jane Doe',
            email='jane@example.com',
            age=45,
            hypertension=True,
            heart_disease=False,
            ever_married=False,
            work_type='Private',
            residence_type='Urban',
            avg_glucose_level=100.0,
            bmi=25.0,
            smoking_status='never smoked',
            stroke=False
        )
        db.session.add(patient)
        db.session.commit()

        self.assertIsNotNone(patient.id)
        self.assertEqual(patient.name, 'Jane Doe')

if __name__ == '__main__':
    unittest.main()
    