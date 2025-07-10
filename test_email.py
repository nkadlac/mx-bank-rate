#!/usr/bin/env python3
"""
Test email functionality
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def test_email():
    """Test email sending functionality"""
    
    # Email configuration - you'll need to update these
    email_sender = "nate@kadlac.com"  # Your Gmail address
    email_password = "YOUR_APP_PASSWORD_HERE"  # Your Gmail app password
    email_recipient = "nate@kadlac.com"  # Where to send the test email
    
    print("Testing email functionality...")
    print(f"From: {email_sender}")
    print(f"To: {email_recipient}")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = "🧪 Test Email - Mexican Bank Rate Checker"
        
        # Email body
        body = """
        <html>
        <body>
            <h2>Test Email from Mexican Bank Rate Checker</h2>
            <p>This is a test email to verify that the email functionality is working correctly.</p>
            <p>If you received this email, the rate checker will be able to send you notifications when significant rate drops occur.</p>
            <br>
            <p><strong>Current Status:</strong> ✅ Email system is working</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Email server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("Starting TLS...")
            server.login(email_sender, email_password)
            print("Login successful!")
            server.send_message(msg)
            print("Email sent successfully!")
        
        print("✅ Test email sent! Check your inbox.")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("Make sure you're using an App Password, not your regular Gmail password.")
        print("Go to: https://myaccount.google.com/apppasswords")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Email Test Script")
    print("=" * 50)
    print("Before running this script:")
    print("1. Update the email_password variable with your Gmail app password")
    print("2. Make sure you have 2-factor authentication enabled on your Gmail")
    print("3. Generate an app password at: https://myaccount.google.com/apppasswords")
    print("=" * 50)
    
    # Check if password is still the placeholder
    if "YOUR_APP_PASSWORD_HERE" in open(__file__).read():
        print("❌ Please update the email_password variable in this script first!")
        print("Replace 'YOUR_APP_PASSWORD_HERE' with your actual Gmail app password.")
    else:
        test_email() 