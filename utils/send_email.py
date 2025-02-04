from email.mime.multipart import MIMEMultipart
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_medical_record(data):
    # Email configuration
    sender_email = "medipredictai@gmail.com"  # Replace with your email
    sender_password = "dgoyocbtfwfjobja"  # Use App Password for Gmail

    # Construct the full path to the logo
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_dir, 'static', 'logo.png')

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Medical Record for {data['name']} - Medipredict Analysis"
    msg['From'] = sender_email
    msg['To'] = data['email']

    # Attach logo
    with open(logo_path, "rb") as img_file:
        logo = MIMEImage(img_file.read())
        logo.add_header('Content-ID', '<logo>')
        msg.attach(logo)

    # Create the email body with HTML formatting
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <img src="cid:logo" alt="Medipredict Logo" style="max-width: 200px; display: block; margin: 0 auto;">
        
        <h1 style="color: #2c3e50; text-align: center;">Medical Record Analysis</h1>
        
        <div style="background-color: #f4f4f4; padding: 20px; border-radius: 10px;">
            <h2 style="color: #3498db;">Patient Details</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Name:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['name']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Email:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['email']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Age:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['age']}</td>
                </tr>
            </table>

            <h2 style="color: #3498db; margin-top: 20px;">Health Indicators</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Hypertension:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['hypertension']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Heart Disease:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['heart_disease']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Marital Status:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['ever_married']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Work Type:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['work_type']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Residence Type:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['residence_type']}</td>
                </tr>
            </table>

            <h2 style="color: #3498db; margin-top: 20px;">Additional Metrics</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Average Glucose Level:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['avg_glucose_level']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>BMI:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['bmi']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Smoking Status:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['smoking_status']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Stroke Risk:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{data['stroke']}</td>
                </tr>
            </table>
        </div>

        <p style="text-align: center; margin-top: 20px; color: #7f8c8d;">
            © 2024 Medipredict. All rights reserved.
        </p>
    </body>
    </html>
    """

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Establish a secure session with Gmail's outgoing SMTP server using your credentials
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, data['email'], msg.as_string())
        server.quit()

        print(f"Medical record email sent successfully to {data['email']}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
