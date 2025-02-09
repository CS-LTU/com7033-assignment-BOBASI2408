import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from utils.send_email import send_medical_record

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'name': 'Test Patient',
            'email': 'test@example.com',
            'age': 30,
            'hypertension': 0,
            'heart_disease': 0,
            'smoking_status': 'never smoked',
            'ever_married': 'No',         # added missing key
            'work_type': 'Private',       # added missing key
            'residence_type': 'Urban',    # added missing key
            'avg_glucose_level': 100,     # added missing key
            'bmi': 25,                    # added missing key
            'stroke': 0                   # added missing key
        }

    def test_send_medical_record_success(self):
        """Test successful email sending"""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value = mock_server
            result = send_medical_record(self.test_data)
            self.assertTrue(result)
            # Changed: assert sendmail was called instead of send_message
            mock_server.sendmail.assert_called_once()

    def test_send_medical_record_missing_data(self):
        """Test handling of missing data"""
        incomplete_data = {'name': 'Test Patient'}
        with patch('smtplib.SMTP'):
            with self.assertRaises(KeyError):
                send_medical_record(incomplete_data)

    @patch('os.path.join')
    def test_logo_path(self, mock_path_join):
        """Test logo path construction"""
        mock_path_join.return_value = '/mock/path/to/logo.png'
        # Provide valid PNG header bytes so MIMEImage can determine the subtype
        with patch('smtplib.SMTP'), patch('builtins.open', unittest.mock.mock_open(read_data=b'\x89PNG\r\n\x1a\ndummy')):
            send_medical_record(self.test_data)
        mock_path_join.assert_called()

    def test_email_content(self):
        """Test email content generation"""
        with patch('smtplib.SMTP') as mock_smtp:
            # Patch the local import in send_email
            with patch('utils.send_email.MIMEMultipart') as mock_mime:
                instance = mock_mime.return_value
                send_medical_record(self.test_data)
                # Verify email construction: attach should be called
                self.assertTrue(instance.attach.called)
                self.assertGreater(instance.attach.call_count, 0)

    def test_smtp_connection_error(self):
        """Test SMTP connection error handling"""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.side_effect = Exception('Connection failed')
            # Instead of raising, function catches exception so expect False
            result = send_medical_record(self.test_data)
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()