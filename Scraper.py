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
    
    """   # Function to automate Google search using Selenium
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
    
    """

    def google_search(self, query, api_key, search_engine_id, num_results=10):
         """
        Perform a Google search using the Custom Search JSON API.

        :param query: Search query string
        :param api_key: Google API key
        :param search_engine_id: Google Custom Search Engine ID (cx)
        :param num_results: Number of results to return (max 10 per request)
        :return: List of search result URLs and titles
        """
         url = "https://www.googleapis.com/customsearch/v1"
         results = []
         params = {
            "q": query,
            "key": api_key,
            "cx": search_engine_id,
            "num": min(num_results, 10)  # Maximum 10 results per request
         }

         try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()

            for item in data.get("items", []):
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link")
                })
         except requests.RequestException as e:
            print(f"Request error: {e}")
         except ValueError as e:
            print(f"Error parsing JSON response: {e}")
    
         return results


     # Function to save emails to a CSV file
    def save_emails_to_csv(self, emails, filename):
         df = pd.DataFrame(emails, columns=['Email'])
         df.drop_duplicates(inplace=True)  # Remove duplicate emails
         df.to_csv(filename, index=False)
         print(f"Saved {len(emails)} emails to {filename}")




if __name__=='__main__':
     scraper = Scraper()
     company_name = input("Enter the company name: ")
     num_results = 10  # Number of Google search results to scrape

     # Replace with your API key and Search Engine ID
     API_KEY = "AIzaSyD_dgWLVfun_TWC4xrxCRHK2q2W_eSnm64"
     SEARCH_ENGINE_ID = "017357165953623309164:4esf1pr-zas"

     #print("[*] Searching Google...")
    #search_results = scraper.google_search(company_name, num_results=num_results)

    # Search query
     search_query = f"{company_name} contact email"

     print(f"Searching for: {search_query}")
     results = scraper.google_search(search_query, API_KEY, SEARCH_ENGINE_ID, 10)


     if results:
        print(f"Found {len(results)} results:")
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. {result['title']}: {result['link']}")
     else:
        print("No results found.")

     

     all_emails = set()  # Use a set to avoid duplicates

     for result in results:
        url = result['link']
        print(f"[*] Scraping {url}")
        html = scraper.get_html(url)
        if html:
            emails = scraper.extract_emails(html)
            all_emails.update(emails)

     if all_emails:
        print(f"[+] Found {len(all_emails)} emails:")
        for email in all_emails:
            print(f"    - {email}")

        # Save emails to CSV
        scraper.save_emails_to_csv(list(all_emails), f"{company_name}_emails.csv")
     else:
        print("[-] No emails found.")

     

