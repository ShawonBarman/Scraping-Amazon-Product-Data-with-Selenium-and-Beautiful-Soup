import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import os

# Read the CSV file
df = pd.read_csv('amazon_data.csv')

# Set up Selenium
chrome_options = Options()
service = Service('./web driver/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create a CSV file and write headers if it doesn't exist
csv_file_path = 'final_amazon_data.csv'
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Category', 'Sub-Category', 'Description', 'Price', 'Ratings', 'Total Ratings', 'Date First Available', 'Product URL'])

# Iterate over each row in the original DataFrame
for index, row in df.iterrows():
    # Extract the product URL
    url = 'https://www.amazon.com' + row['Product URL']
    
    # Open the URL with delay
    time.sleep(5)  # Adjust the delay time as needed
    driver.get(url)
    
    # Scrape the description
    description = ''
    try:
        description_element = driver.find_element(By.ID, 'productDescription')
        if description_element:
            description = description_element.text
    except NoSuchElementException:
        print('Description element not found. Skipping...')
    
    # Scrape the date first available
    date_first_available = ''
    try:
        date_available_element = driver.find_element(By.XPATH, '//table[@id="productDetails_detailBullets_sections1"]/tbody/tr[last()]/td')
        if date_available_element:
            date_first_available = date_available_element.text
    except NoSuchElementException:
        print('Date First Available element not found. Skipping...')
    
    # Remove quotation marks from the Title
    title = row['Title'].strip('"')
    
    # Add the data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([title, row['Category'], row['Sub-Category'], description, row['Price'], row['Ratings'], row['Total Ratings'], date_first_available, 'https://www.amazon.com' + row['Product URL']])

    print(title, "Done!")

# Save the new DataFrame to a CSV file
print("All data saved done")
# Quit the Selenium WebDriver
driver.quit()
