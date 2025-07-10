#!/usr/bin/env python3
"""
Debug email functionality with detailed error reporting
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def debug_email():
    """Debug email sending with detailed error reporting"""
    
    print("=" * 60)
    print("EMAIL DEBUG SCRIPT")
    print("=" * 60)
    
    # Check environment variables
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_recipient = os.getenv('EMAIL_RECIPIENT')
    
    print(f"EMAIL_SENDER: {email_sender}")
    print(f"EMAIL_PASSWORD: {'*' * len(email_password) if email_password else 'NOT SET'}")
    print(f"EMAIL_RECIPIENT: {email_recipient}")
    print()
    
    if not all([email_sender, email_password, email_recipient]):
        print("❌ Missing environment variables!")
        print("Make sure EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENT are set.")
        return
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = "🔍 Email Debug Test - Mexican Rate Checker"
        
        body = """
        <html>
        <body>
            <h2>Email Debug Test</h2>
            <p>This is a debug email to test the email functionality.</p>
            <p>If you receive this, the email system is working correctly.</p>
            <p><strong>Timestamp:</strong> Debug test</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        
        # Test connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("✅ SMTP connection established")
        
        # Start TLS
        server.starttls()
        print("✅ TLS started")
        
        # Login
        print("Attempting login...")
        server.login(email_sender, email_password)
        print("✅ Login successful!")
        
        # Send email
        print("Sending email...")
        server.send_message(msg)
        print("✅ Email sent successfully!")
        
        # Close connection
        server.quit()
        print("✅ Connection closed")
        
        print("\n🎉 SUCCESS: Email debug test completed!")
        print("Check your inbox for the debug email.")
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ AUTHENTICATION ERROR: {e}")
        print("\nCommon solutions:")
        print("1. Make sure you're using an App Password, not your regular Gmail password")
        print("2. Generate a new App Password at: https://myaccount.google.com/apppasswords")
        print("3. Make sure 2-Factor Authentication is enabled on your Gmail account")
        print("4. Remove spaces from the App Password when adding to GitHub secrets")
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("Check your internet connection and firewall settings.")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    debug_email() 