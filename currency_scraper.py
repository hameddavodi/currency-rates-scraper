import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import pandas as pd

def scrape_currency_rates():
    """
    Scrape currency and gold rates from Bonbast website
    """
    try:
        # URL of the website
        url = "https://www.bonbast.com/"
        
        # Send an HTTP request to the website
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for request errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the desired values
        usd_value = soup.find('td', {'id': 'usd1'}).text.strip()
        eur_value = soup.find('td', {'id': 'eur1'}).text.strip()
        azadi_value = soup.find('td', {'id': 'azadi12'}).text.strip()
        bitcoin_value = soup.find('span', {'id': 'bitcoin'}).text.strip()
        
        # Get the current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d')
        current_time = current_datetime.strftime('%H:%M:%S')
        full_timestamp = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare data for logging
        data = {
            'Timestamp': full_timestamp,
            'Date': current_date,
            'Time': current_time,
            'USD': usd_value,
            'EUR': eur_value,
            'Azadi': azadi_value,
            'Bitcoin': bitcoin_value
        }
        
        # Log to CSV
        log_to_csv(data)
        
        # Print the results
        print(f"Timestamp: {full_timestamp}")
        print(f"USD Value: {usd_value}")
        print(f"EUR Value: {eur_value}")
        print(f"Azadi Value: {azadi_value}")
        print(f"Bitcoin Value: {bitcoin_value}")
        
        return data
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except AttributeError as e:
        print(f"Error parsing website content: {e}")
        return None

def log_to_csv(new_data):
    """
    Log scraped data to a CSV file
    Appends new data or creates a new file if it doesn't exist
    """
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # CSV file path
    csv_file = 'logs/currency_rates.csv'
    
    # Check if file exists
    if os.path.exists(csv_file):
        # Read existing data
        df = pd.read_csv(csv_file)
        
        # Convert new data to DataFrame
        new_df = pd.DataFrame([new_data])
        
        # Append new data
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        # Create new DataFrame if file doesn't exist
        df = pd.DataFrame([new_data])
    
    # Save updated DataFrame
    df.to_csv(csv_file, index=False)

def main():
    scrape_currency_rates()

if __name__ == "__main__":
    main()
