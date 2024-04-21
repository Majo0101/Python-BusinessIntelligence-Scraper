import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class Scrapper:
      def __init__(self, isin):
            self.isin = isin
            self.driver = self.initialize_driver()
            self.navigate_to_site()
            self.accept_cookies()
            self.click_expand_links()
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

      def initialize_driver(self):
            driver_path = 'geckodriver.exe'
            firefox_binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'
            service = FirefoxService(executable_path=driver_path)
            options = FirefoxOptions()
            options.binary_location = firefox_binary
            options.add_argument("--headless")
            return webdriver.Firefox(service=service, options=options)

      def navigate_to_site(self):
            self.driver.get(f'https://www.justetf.com/en/etf-profile.html?isin={self.isin}')
            print(self.driver.title)
            time.sleep(3)

      def accept_cookies(self):
            try:
                  cookie_button = WebDriverWait(self.driver, 10).until(
                  EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"))
                  )
                  cookie_button.click()
                  print("Cookie consent accepted.")
                  time.sleep(1)
            except Exception as e:
                  print("Could not find or click the cookie button:", e)

      def click_expand_links(self):
            clicked = 0
            links = self.driver.find_elements(By.CLASS_NAME, 'expand-link')
            for link in links:
                  try:
                        link.click()
                        clicked += 1
                        time.sleep(0.1)
                  except Exception:
                        pass
            print(f'Clicked {clicked} times !')
            time.sleep(1)

      def catch_data(self,column1, column2):
            results = []
            h3_data = self.soup.find('h3', string=' Data ')
            if h3_data:
                  table = h3_data.find_next('table')
                  if table:
                        tbody = table.find('tbody')
                        if tbody:
                              for row in tbody.find_all('tr'):
                                    cells = row.find_all('td')
                                    if len(cells) >= 2:
                                          row_data = {
                                                column1: cells[0].text.strip(),
                                                column2: cells[1].text.strip()
                                          }
                                          results.append(row_data)
                        else:
                              print("No tbody found within the table.")
                  else:
                        print("No table found directly following the 'Data' <h3> tag.")
            else:
                  print("No <h3> tag with the text 'Data' found.")

            return results
      
      def catch_countries(self, column1, column2):
            results = []
            h3_countries = self.soup.find('h3', string=' Countries ')
            if h3_countries:
                  table = h3_countries.find_next_sibling('table')
                  if table:
                        for row in table.find_all('tr'):
                              cells = row.find_all('td')
                              if len(cells) >= 2:
                                    row_data = {
                                          column1: cells[0].text.strip(),
                                          column2: cells[1].text.strip()
                                    }
                                    results.append(row_data)
                  else:
                        print("No table found after the specified <h3> tag.")
            else:
                  print("No <h3> tag with the title 'Countries' found.")

            return results
      
      def catch_sectors(self, column1, column2):
            results = []
            h3_sectors = self.soup.find('h3', string=' Sectors ') 
            if h3_sectors:
                  table = h3_sectors.find_next_sibling('table')
                  if table:
                        for row in table.find_all('tr'):
                              cells = row.find_all('td')
                              if len(cells) >= 2:
                                    row_data = {
                                          column1: cells[0].text.strip(),
                                          column2: cells[1].text.strip()
                                    }
                                    results.append(row_data)
                  else:
                        print("No table found after the specified <h3> tag.")
            else:
                  print("No <h3> tag with the title 'Countries' found.")

            return results
      
      def catch_holdings(self, column1, column2):
            results = []
            div_constituents_top = self.soup.find('div', class_='constituents-top')
            if div_constituents_top:
                  table = div_constituents_top.find_next_sibling('table')
                  if table:
                        tbody = table.find('tbody')
                        if tbody:
                              for row in tbody.find_all('tr'):
                                    cells = row.find_all('td')
                                    if len(cells) >= 2:
                                          row_data = {
                                                column1: cells[0].text.strip(),
                                                column2: cells[1].text.strip()
                                          }
                                          results.append(row_data)
                        else:
                              print("No tbody found within the table.")
                  else:
                        print("No table found within the 'constituents-top' class.")
            else:
                  print("No div with the class 'constituents-top' found.")

            return results
      
      def real_time_data(self, column1, column2):
            results = []
            realtime_quotes = self.soup.find('div', id='realtime-quotes')
            if realtime_quotes:
                  vals = realtime_quotes.find_all(class_='val')
                  if vals and len(vals) >= 2:
                        row_data = {
                              column1: vals[0].text.strip() + " " + vals[1].text.strip(),
                              column2: column2
                        }
                        results.append(row_data)
                  else:
                        print("Less than two elements with class 'val' found within 'realtime-quotes'.")
            else:
                  print("No element with the ID 'realtime-quotes' found.")

            return results

      def close(self):
            self.driver.quit()
            print('Driver was closed !')
            time.sleep(2)