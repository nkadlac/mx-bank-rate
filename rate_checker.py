#!/usr/bin/env python3
"""
Mexican Bank Rate Checker
Checks for drops in Mexican bank rate and sends email notifications.
"""

import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MexicanRateChecker:
    def __init__(self):
        self.api_base_url = "https://www.banxico.org.mx/SieAPIRest/service/v1"
        self.api_key = os.getenv('BANXICO_API_KEY', 'fe98b823e1f97117bb9263c7dfb00a0434ab5d30ac5a1c0853c23641f72b77bc')
        self.email_sender = os.getenv('EMAIL_SENDER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_recipient = os.getenv('EMAIL_RECIPIENT')
        
        # Validate required environment variables
        if not all([self.email_sender, self.email_password, self.email_recipient]):
            raise ValueError("Missing required environment variables: EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT")
    
    def get_current_rate(self):
        """Get the current Mexican bank rate from Banxico API"""
        try:
            # Banxico API endpoint for interest rate (SF43718 is the series ID for target rate)
            url = f"{self.api_base_url}/series/SF43936/datos/oportuno"
            
            headers = {
                'Bmx-Token': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'bmx' in data and 'series' in data['bmx']:
                series = data['bmx']['series'][0]
                if 'datos' in series and series['datos']:
                    latest_data = series['datos'][0]
                    rate = float(latest_data['dato'])
                    date = latest_data['fecha']
                    logger.info(f"Current rate: {rate}% as of {date}")
                    return rate, date
            
            raise ValueError("No rate data found in API response")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching rate data: {e}")
            raise
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Error parsing rate data: {e}")
            raise
    
    def get_historical_rate(self, days_back=7, current_date=None):
        """Get historical rate data for comparison"""
        try:
            # Get data for the last N days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            url = f"{self.api_base_url}/series/SF43936/datos/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            
            headers = {
                'Bmx-Token': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'bmx' in data and 'series' in data['bmx']:
                series = data['bmx']['series'][0]
                if 'datos' in series and len(series['datos']) >= 1:
                    # Find the most recent data point that is NOT the current date
                    for entry in reversed(series['datos']):
                        if current_date is None or entry['fecha'] != current_date:
                            historical_rate = float(entry['dato'])
                            historical_date = entry['fecha']
                            logger.info(f"Historical rate: {historical_rate}% as of {historical_date}")
                            return historical_rate, historical_date
                    raise ValueError("No suitable historical rate data found (all entries are for today)")
            
            raise ValueError("No historical rate data found")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching historical data: {e}")
            raise
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Error parsing historical data: {e}")
            raise
    
    def calculate_rate_change(self, current_rate, historical_rate):
        """Calculate the rate change in basis points"""
        change_bp = (historical_rate - current_rate) * 100  # Convert to basis points
        return change_bp
    
    def send_email_notification(self, current_rate, historical_rate, change_bp, current_date, historical_date):
        """Send email notification about rate drop"""
        try:
            # Email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_recipient
            msg['Subject'] = f"🚨 Mexican Bank Rate Drop Alert: {change_bp:.1f} bp"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>Mexican Bank Rate Drop Alert</h2>
                <p><strong>Rate Change:</strong> {change_bp:.1f} basis points</p>
                <p><strong>Current Rate:</strong> {current_rate}% (as of {current_date})</p>
                <p><strong>Previous Rate:</strong> {historical_rate}% (as of {historical_date})</p>
                <p><strong>Change:</strong> {historical_rate - current_rate:.2f} percentage points</p>
                <br>
                <p>This alert was triggered because the rate dropped by at least 50 basis points.</p>
                <p>Source: <a href="https://www.banxico.org.mx">Banco de México</a></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent successfully to {self.email_recipient}")
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            raise
    
    def check_rate_drop(self, threshold_bp=50):
        """Main function to check for rate drops"""
        try:
            logger.info("Starting Mexican bank rate check...")
            
            # Get current and historical rates
            current_rate, current_date = self.get_current_rate()
            historical_rate, historical_date = self.get_historical_rate(current_date=current_date)
            
            # Calculate rate change
            change_bp = self.calculate_rate_change(current_rate, historical_rate)
            
            logger.info(f"Rate change: {change_bp:.1f} basis points")
            
            # Check if drop meets threshold
            if change_bp >= threshold_bp:
                logger.info(f"Rate drop threshold met! Sending notification...")
                self.send_email_notification(
                    current_rate, historical_rate, change_bp, 
                    current_date, historical_date
                )
                return True
            else:
                logger.info(f"Rate drop ({change_bp:.1f} bp) below threshold ({threshold_bp} bp). No notification sent.")
                return False
                
        except Exception as e:
            logger.error(f"Error in rate check: {e}")
            raise

def main():
    """Main entry point"""
    try:
        checker = MexicanRateChecker()
        # Temporarily set threshold to 0 to force email for testing
        checker.check_rate_drop(threshold_bp=25)
        logger.info("Rate check completed successfully")
    except Exception as e:
        logger.error(f"Rate check failed: {e}")
        exit(1)

if __name__ == "__main__":
    main() 