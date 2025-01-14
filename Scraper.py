import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from fake_useragent import UserAgent

class Scraper:

    # Function to get HTML content using requests
    def get_html(self, url):
        headers = {'User-Agent': UserAgent().random}  # Rotate user-agent to avoid blocks
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}. Status Code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        return None

    
    def beautiful_html(self, html):
        return BeautifulSoup(html)
    
    def extract_emails(self, html):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, html)
    
    # Function to automate Google search using Selenium
    def google_search(self, company_name, num_results=5):
        search_query = f"{company_name} contact email"
        search_results = []
        
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f'user-agent={UserAgent().random}')

        driver = webdriver.Chrome(options=chrome_options, service=Service("/users/mprataps/Downloads/ChromeDriver/chromedriver"))  # Replace with actual path to ChromeDriver

        try:
            driver.get("https://www.google.com")
            sleep(2)  # Wait for page to load
            
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(search_query + Keys.RETURN)
            sleep(3)  # Wait for search results
            
            links = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']//a")
            for link in links[:num_results]:
                search_results.append(link.get_attribute("href"))
        except Exception as e:
            print(f"Error during Google search: {e}")
        finally:
            driver.quit()

        return search_results





if __name__=='__main__':
     scraper = Scraper()
     company_name = input("Enter the company name: ")
     num_results = 5  # Number of Google search results to scrape

     print("[*] Searching Google...")
     search_results = scraper.google_search(company_name, num_results=num_results)

     print(search_results)

     all_emails = set()  # Use a set to avoid duplicates


