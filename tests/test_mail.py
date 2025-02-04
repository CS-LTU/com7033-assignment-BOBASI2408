import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the function to test
from utils.send_email import send_medical_record

class TestEmailService(unittest.TestCase):
    def setUp(self):
        # Sample test data that matches the structure in your original function
        self.test_data = {
            "name": "John Doe",
            "email": "test@example.com",
            "age": 45,
            "work_type": "Private",
            "residence_type": "Urban",
            "avg_glucose_level": 145.5,
            "bmi": 28.2,
            "smoking_status": "Formerly Smoked",
            "hypertension": True,
            "heart_disease": False,
            "ever_married": True,
            "stroke": True
        }

    def test_send_medical_record_success(self):
        """
        Test successful email sending
        """
        # Mock the SMTP server to simulate successful email sending
        with patch('smtplib.SMTP') as mock_smtp:
            # Create a mock instance
            mock_server = MagicMock()
            mock_smtp.return_value = mock_server

            # Call the function
            result = send_medical_record(self.test_data)

            # Assertions
            self.assertTrue(result)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.sendmail.assert_called_once()
            mock_server.quit.assert_called_once()

    def test_send_medical_record_missing_data(self):
        """
        Test email sending with incomplete data
        """
        # Create a copy of test data and remove a key
        incomplete_data = self.test_data.copy()
        del incomplete_data['name']

        with self.assertRaises(KeyError):
            send_medical_record(incomplete_data)

    @patch('os.path.join')
    def test_logo_path_construction(self, mock_path_join):
        """
        Test that the logo path is constructed correctly
        """
        # Mock the path joining to verify it's called with correct arguments
        mock_path_join.return_value = '/mock/path/to/logo.png'

        with patch('smtplib.SMTP'), patch('builtins.open', unittest.mock.mock_open()):
            send_medical_record(self.test_data)

        # Check if path.join was called with expected arguments
        mock_path_join.assert_called()

    def test_email_content(self):
        """
        Test that email content is generated correctly
        """
        with patch('smtplib.SMTP'):
            with patch('email.mime.multipart.MIMEMultipart') as mock_mime:
                send_medical_record(self.test_data)
                
                # Verify that the subject is set correctly
                mock_mime.return_value.__setitem__.assert_any_call(
                    'Subject', f"Medical Record for {self.test_data['name']} - Medipredict Analysis"
                )

    @patch('smtplib.SMTP')
    def test_exception_handling(self, mock_smtp):
        """
        Test exception handling during email sending
        """
        # Simulate an SMTP server login failure
        mock_smtp.return_value.login.side_effect = Exception("Connection failed")

        result = send_medical_record(self.test_data)
        
        # Verify the function returns False on exception
        self.assertFalse(result)

    def test_required_fields(self):
        """
        Ensure all required fields are present in the data
        """
        required_fields = [
            'name', 'email', 'age', 'work_type', 'residence_type', 
            'avg_glucose_level', 'bmi', 'smoking_status', 
            'hypertension', 'heart_disease', 'ever_married', 'stroke'
        ]
        
        for field in required_fields:
            with self.subTest(field=field):
                data_copy = self.test_data.copy()
                del data_copy[field]
                
                with self.assertRaises(KeyError):
                    send_medical_record(data_copy)

if __name__ == '__main__':
    unittest.main()