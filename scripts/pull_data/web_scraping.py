import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from datetime import date
from pathlib import Path

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data = None
        self.webscrape_df = None
        
    def fetch_data(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
     
    # Extracts and splits launch date and time from table cell   
    def date_time(self, table_cells):
        return [data_time.strip() for data_time in list(table_cells.strings)][0:2]
    
    # Extracts launch booster version name
    def booster_version(self, table_cells):
        booster = ' '.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i%2==0][0:-1])
        return booster
    # Extracts payload mass
    def get_mass(self, table_cells):
        mass=unicodedata.normalize('NFKD', table_cells.text).strip()
        if mass:
            new_mass=mass[0:mass.find('kg')+2]
        else:
            new_mass=0
        return new_mass
    
    # Extracts landing_status
    def landing_status(self, table_cells):
        status = list(table_cells.strings)[0]
        return status
        
        
    def extract_data(self):
        
        # Initializes dictionary to store flattened data for the final DataFrame
        self.data = {}
        
        self.data['Flight No.'] = []
        self.data['Launch site'] = []
        self.data['Payload'] = []
        self.data['Payload mass'] = []
        self.data['Orbit'] = []
        self.data['Customer'] = []
        self.data['Launch outcome'] = []
        self.data['Version Booster']=[]
        self.data['Booster landing']=[]
        self.data['Date']=[]
        self.data['Time']=[]
        
        extracted_row = 0
        
        # Iterates through all launch tables and rows, extracting and flattening data
        for table_number, table in enumerate(self.soup.find_all('table', 'wikitable plainrowheaders collapsible')):
            for rows in table.find_all('tr'):
                # Loops through each row to check if it contains a <th> tag.
                if rows.th:
                    # If the row has a <th> tag, checks whether it contains any nested HTML tags.
                    if rows.th.string:
                        # If there are no nested tags, extracts the string, strips whitespace, and checks if it is entirely numeric.
                        flight_number= rows.th.string.strip()
                        flag=flight_number.isdigit()
                    else:
                        # If there are nested tags, extracts the first string from the nested tag, strips it, and checks if it's numeric.
                        flight_number=list(rows.th.strings)[0].strip()
                        flag=flight_number.isdigit()
                else: flag=False
                
                row=rows.find_all('td')
                
                if flag:
                    extracted_row += 1
                    # Extracts and Appends flight number
                    self.data['Flight No.'].append(flight_number)
                    datetimelist=self.date_time(row[0])
                    
                    # Extracts and Appends launch date
                    self.data['Date'].append(datetimelist[0])
                    date = datetimelist[0].strip(',')
                    
                    # Extracts and Appends launch time
                    self.data['Time'].append(datetimelist[1])
                    time = datetimelist[1]
                    
                    # Extracts and appends booster version; falls back to <a> tag if necessary
                    bv = self.booster_version(row[1])
                    if not(bv):
                        bv=row[1].a.string
                    self.data['Version Booster'].append(bv)
                    
                    # Extracts and Appends launch site name
                    launch_site = row[2].a.string
                    self.data['Launch site'].append(launch_site)
                    
                    # Extracts and Appends payload name
                    payload = row[3].a.string
                    self.data['Payload'].append(payload)
                    
                    # Extracts and appends payload_mass
                    payload_mass = self.get_mass(row[4])
                    self.data['Payload mass'].append(payload_mass)
                    
                    # Extracts and appends orbit name
                    orbit = row[5].a.string
                    self.data['Orbit'].append(orbit)
                    
                    # Extracts and appends customer name
                    customer = None
                    if row[6].a:
                        customer = row[6].a.string
                    else:
                        customer = row[6].string
                    self.data['Customer'].append(customer)
                    
                    # Extracts and appends launch outcome
                    launch_outcome = list(row[7].strings)[0]
                    self.data['Launch outcome'].append(launch_outcome)
                    
                    # Extract and appends booster landing
                    booster_landing = self.landing_status(row[8])
                    self.data['Booster landing'].append(booster_landing)
                    
                    self.webscrape_df = pd.DataFrame(self.data)
    
    # Saves the extracted data as a CSV file in the raw_data directory              
    def save_data(self):
        root_dir = Path(__file__).resolve().parent.parent.parent
        raw_data_path = root_dir/'data'/'raw_data'
        raw_data_path.mkdir(parents=True, exist_ok=True)

        today = date.today().strftime("%Y_%m_%d")

        csv_path = raw_data_path/f'spaceX_webscrape_data_{today}.csv'

        self.webscrape_df.to_csv(csv_path, index=False)
        
    # Executes full scraping pipeline: fetches, extracts, and saves data
    def pull_api_data(self):
        webscrape_data.fetch_data()
        webscrape_data.extract_data()
        webscrape_data.save_data()

webscrape_data = WebScraper(static_url)

webscrape_data.pull_api_data()

        