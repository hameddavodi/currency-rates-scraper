import asyncio
import os
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright

class ValueExtractor:
    def __init__(self, url):
        self.url = url
        self.selectors = {
            'bitcoin': 'span#bitcoin.same_val',
            'gold': 'span#gol18.same_val', 
            'azadi': 'td#azadi1.same_val',
            'usd': 'td#usd1.same_val'
        }

    def log_to_csv(self, new_data):
        """
        Log scraped data to a CSV file
        Appends new data or creates a new file if it doesn't exist
        """
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # CSV file path
        csv_file = 'logs/currency_rates.csv'
        
        # Add timestamp to the data
        new_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
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
        print(f"Data logged to {csv_file}")

    async def extract_values(self):
        """
        Extract specific values using targeted CSS selectors
        """
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            
            # Create a new page
            page = await browser.new_page()
            
            try:
                # Navigate to the specified URL
                await page.goto(self.url, wait_until='networkidle')
                
                # Dictionary to store extracted values
                extracted_values = {}
                
                # Extract values for each selector
                for key, selector in self.selectors.items():
                    try:
                        # Try to get the inner text of the element
                        value = await page.inner_text(selector)
                        extracted_values[key] = value.strip()
                    except Exception as e:
                        extracted_values[key] = f"Could not extract: {str(e)}"
                
                # Log the extracted values to CSV
                self.log_to_csv(extracted_values)
                
                return extracted_values
            
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
            
            finally:
                # Close browser
                await browser.close()

    @classmethod
    async def run(cls, url):
        """
        Class method to run the extractor
        """
        extractor = cls(url)
        return await extractor.extract_values()

# Example usage
async def main():
    url = 'https://www.bonbast.com/' 

    result = await ValueExtractor.run(url)
    
    if result:
        print("Extracted Values:")
        for key, value in result.items():
            print(f"{key.capitalize()}: {value}")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())
