from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Import the necessary modules
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import os

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Add this line to enable headless mode
chrome_options.add_argument("--disable-gpu")  # Add this line to disable GPU acceleration (for headless mode)
service = Service('./web driver/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Send a GET request to the URL
url = "https://www.amazon.com"
driver.get(url)

# Find the search bar element
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")

# Clear any existing text in the search bar
search_bar.clear()

# Enter the search query
Category = "tshirt"
Sub_Category = "tshirt for mens"
search_query = Category + " " + Sub_Category
search_bar.send_keys(search_query)

# Find and click the search button
search_button = driver.find_element(By.ID, "nav-search-submit-button")
search_button.click()

# Create a CSV file and write headers if it doesn't exist
csv_file_path = 'amazon_data.csv'
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Category', 'Sub-Category', 'Price', 'Ratings', 'Total Ratings', 'Product URL'])

# Scrape product details
def scrape_product_details():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products:
        # Handle missing title information
        title_element = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        if title_element:
            title_element = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
        else:
            title_element = product.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
        title = title_element.text.strip() if title_element else ""
        
        # Handle missing price information
        price_element = product.find("span", {"class": "a-price-whole"})
        price = price_element.text.strip() if price_element else ""
        
        # Handle missing ratings information
        ratings_element = product.find("i", {"class": "a-icon-star-small"})
        ratings = ratings_element.find("span", {"class": "a-icon-alt"}).text.strip().split()[0] if ratings_element else ""
        
        # Handle missing total ratings information
        total_ratings_element = product.find("span", {"class": "a-size-base s-underline-text"})
        total_ratings = total_ratings_element.text.strip() if total_ratings_element else ""
        
        # Handle missing product URL
        product_url_element = product.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        product_url = product_url_element["href"] if product_url_element else ""
        
        # Print or save the scraped data as per your requirement
        print("---")
        print("Title:", title)
        print("Category:", Category)
        print("Sub-Category:", Sub_Category)
        print("Price:", price)
        print("Ratings:", ratings)
        print("Total Ratings:", total_ratings)
        print("Product URL:", product_url)
        
        # Check if the data already exists in the CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == title and row[3] == price and row[4] == ratings and row[5] == total_ratings and row[6] == product_url:
                    print(f"Data for '{title}' already exists. Skipping...")
                    return
                
        # Add the data to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, "Sports & Fitness", "Sports Gear (Cycling)", price, ratings, total_ratings, product_url])

# Scrape product details from the current page
scrape_product_details()

# Continue scraping on next pages
while True:
    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]')
        if not next_button.is_enabled():
            break

        next_button.click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "s-pagination-next")]')))
        scrape_product_details()
    except NoSuchElementException:
        break

# Close the browser
driver.quit()