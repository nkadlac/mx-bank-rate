# Mexican Bank Rate Checker

A simple automated system that checks for drops in the Mexican bank rate and sends email notifications when significant changes occur.

## Features

- ✅ **Free GitHub Actions**: Runs automatically without any hosting costs
- ✅ **Bank of Mexico API**: Uses the official Banxico API to get real-time rate data
- ✅ **Weekly Monitoring**: Checks every Monday at 9:00 AM UTC
- ✅ **Email Alerts**: Sends notifications when rate drops by 50+ basis points
- ✅ **Configurable**: Easy to customize threshold and schedule
- ✅ **Invisible Operation**: Runs in the background with minimal maintenance

## How It Works

1. **Data Source**: Fetches current and historical interest rates from [Banco de México](https://www.banxico.org.mx)
2. **Analysis**: Compares current rate with historical data to calculate changes
3. **Alerting**: Sends email notifications when rate drops meet the threshold (50 basis points)
4. **Scheduling**: Runs automatically via GitHub Actions every week

## Quick Start

1. **Fork this repository** to your GitHub account
2. **Set up email credentials** (see [SETUP.md](SETUP.md) for detailed instructions)
3. **Configure GitHub Secrets** with your email settings
4. **Enable GitHub Actions** in your repository
5. **Test manually** by triggering the workflow from the Actions tab

## Files Overview

- `rate_checker.py` - Main Python script that checks rates and sends notifications
- `.github/workflows/rate-check.yml` - GitHub Actions workflow configuration
- `requirements.txt` - Python dependencies
- `SETUP.md` - Detailed setup and configuration guide

## Configuration

### Email Setup
- Uses Gmail SMTP for sending notifications
- Requires App Password (not regular password)
- Supports custom sender and recipient addresses

### Rate Threshold
- Default: 50 basis points (0.5 percentage points)
- Easily configurable in the code
- Calculates change from current vs. historical rates

### Schedule
- Default: Every Monday at 9:00 AM UTC
- Configurable via cron expression
- Supports manual triggering for testing

## API Information

This project uses the [Banco de México API](https://www.banxico.org.mx/SieAPIRest/service/v1) to fetch:
- Current target interest rate (series SF43718)
- Historical rate data for comparison
- Real-time updates from official sources

## License

This project is open source and available under the MIT License. 