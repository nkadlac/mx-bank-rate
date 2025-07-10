# Setup Guide

## Prerequisites

1. A GitHub account
2. A Gmail account (for sending notifications)
3. Python 3.11+ (for local testing)

## Email Setup

### Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Use this app password (not your regular Gmail password)

## GitHub Secrets Configuration

You need to set up the following secrets in your GitHub repository:

1. Go to your repository on GitHub
2. Click on "Settings" → "Secrets and variables" → "Actions"
3. Add the following repository secrets:

### Required Secrets

- `EMAIL_SENDER`: Your Gmail address (e.g., `your-email@gmail.com`)
- `EMAIL_PASSWORD`: Your Gmail app password (not your regular password)
- `EMAIL_RECIPIENT`: Email address to receive notifications (can be the same as sender)
- `BANXICO_API_KEY`: Your Bank of Mexico API key (optional - a default key is provided)

## Local Testing

To test the script locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export EMAIL_SENDER="nate@kadlac.com"
   export EMAIL_PASSWORD="lheyzbupuyzxldsy"
   export EMAIL_RECIPIENT="nate@kadlac.com"
   # Optional: Set custom API key (default key is already included)
   export BANXICO_API_KEY="fe98b823e1f97117bb9263c7dfb00a0434ab5d30ac5a1c0853c23641f72b77bc"
   ```

3. Run the script:
   ```bash
   python rate_checker.py
   ```

## GitHub Actions

The workflow is configured to run:
- **Automatically**: Every Monday at 9:00 AM UTC
- **Manually**: You can trigger it from the "Actions" tab in your repository

## Customization

### Change Schedule
Edit `.github/workflows/rate-check.yml` and modify the cron expression:
```yaml
- cron: '0 9 * * 1'  # Monday 9 AM UTC
```

### Change Threshold
Edit `rate_checker.py` and modify the threshold in the `check_rate_drop()` call:
```python
checker.check_rate_drop(threshold_bp=50)  # 50 basis points
```

### Change Email Provider
The script is configured for Gmail. For other providers, modify the SMTP settings in `send_email_notification()`.

## Troubleshooting

### Common Issues

1. **Email not sending**: Make sure you're using an App Password, not your regular Gmail password
2. **API errors**: Check if the Banxico API is accessible from your location
3. **Workflow not running**: Check if the repository has Actions enabled and secrets are configured

### Debug Mode

To see more detailed logs, you can modify the logging level in `rate_checker.py`:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
``` 

Fantastic! 🎉 That means your email notifications are working perfectly!

## Next Steps

1. **Restore the Threshold**  
   Since you set the threshold to 0 for testing, you should now change it back to `50` basis points for real monitoring.  
   - In `rate_checker.py`, find:
     ```python
     checker.check_rate_drop(threshold_bp=0)
     ```
   - Change it back to:
     ```python
     checker.check_rate_drop(threshold_bp=50)
     ```
   - Commit and push this change.

2. **(Optional) Remove Debug Scripts**  
   If you want, you can remove or comment out the debug email step from your workflow and delete `debug_email.py` to keep things clean.

3. **Let It Run Automatically**  
   Your workflow will now check the rate every day and only email you if the drop is 50 basis points or more.

---

**You’re all set!**  
If you ever want to test again, just lower the threshold temporarily.  
If you need more features (like logging, multiple recipients, or Slack alerts), just ask! 