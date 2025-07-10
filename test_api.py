#!/usr/bin/env python3
"""
Test script to verify Bank of Mexico API connectivity
"""

import requests
import json

def test_banxico_api():
    """Test the Bank of Mexico API connectivity"""
    print("Testing Bank of Mexico API connectivity...")
    
    # API key (you can also set this as environment variable BANXICO_API_KEY)
    api_key = "fe98b823e1f97117bb9263c7dfb00a0434ab5d30ac5a1c0853c23641f72b77bc"
    
    try:
        # Test current rate endpoint
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
        
        headers = {
            'Bmx-Token': api_key,
            'Content-Type': 'application/json'
        }
        
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print("✅ API connection successful!")
        print(f"Response status: {response.status_code}")
        
        # Parse and display the data
        if 'bmx' in data and 'series' in data['bmx']:
            series = data['bmx']['series'][0]
            if 'datos' in series and series['datos']:
                latest_data = series['datos'][0]
                rate = float(latest_data['dato'])
                date = latest_data['fecha']
                print(f"✅ Current Mexican bank rate: {rate}% (as of {date})")
            else:
                print("❌ No rate data found in response")
        else:
            print("❌ Unexpected API response format")
            print(f"Response: {json.dumps(data, indent=2)}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        return False
    
    return True

def test_historical_data():
    """Test historical data endpoint"""
    print("\nTesting historical data endpoint...")
    
    # API key (you can also set this as environment variable BANXICO_API_KEY)
    api_key = "fe98b823e1f97117bb9263c7dfb00a0434ab5d30ac5a1c0853c23641f72b77bc"
    
    try:
        # Test historical data endpoint (last 7 days)
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/2024-01-01/2024-01-31"
        
        headers = {
            'Bmx-Token': api_key,
            'Content-Type': 'application/json'
        }
        
        print(f"Fetching historical data from: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'bmx' in data and 'series' in data['bmx']:
            series = data['bmx']['series'][0]
            if 'datos' in series and series['datos']:
                print(f"✅ Historical data available: {len(series['datos'])} data points")
                # Show first and last entries
                first = series['datos'][-1]
                last = series['datos'][0]
                print(f"   First: {first['fecha']} - {first['dato']}%")
                print(f"   Last:  {last['fecha']} - {last['dato']}%")
            else:
                print("❌ No historical data found")
        else:
            print("❌ Unexpected historical data response format")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Historical data API failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error parsing historical data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Bank of Mexico API Test")
    print("=" * 50)
    
    # Test current rate
    current_success = test_banxico_api()
    
    # Test historical data
    historical_success = test_historical_data()
    
    print("\n" + "=" * 50)
    if current_success and historical_success:
        print("✅ All tests passed! API is working correctly.")
        print("You can now set up the GitHub Actions workflow.")
    else:
        print("❌ Some tests failed. Please check your internet connection and try again.")
    print("=" * 50) 