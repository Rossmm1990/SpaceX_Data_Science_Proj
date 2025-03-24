import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

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
        
    def date_time(self, table_cells):
        return [data_time.strip() for data_time in list(table_cells.strings)][0:2]
    
    def booster_version(self, table_cells):
        booster = ' '.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i%2==0][0:-1])
        return booster
    
    def get_mass(self, table_cells):
        mass=unicodedata.normalize('NFKD', table_cells.text).strip()
        if mass:
            new_mass=mass[0:mass.find('kg')+2]
        else:
            new_mass=0
        return new_mass

    def landing_status(self, table_cells):
        status = list(table_cells.strings)[0]
        return status
        
        
    def extract_data(self):
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
        for table_number, table in enumerate(self.soup.find_all('table', 'wikitable plainrowheaders collapsible')):
            for rows in table.find_all('tr'):
                if rows.th:
                    if rows.th.string:
                        flight_number= rows.th.string.strip()
                        flag=flight_number.isdigit()
                    else:
                        flight_number=list(rows.th.strings)[0].strip()
                        flag=flight_number.isdigit()
                else: flag=False
                
                row=rows.find_all('td')
                
                if flag:
                    extracted_row += 1
                    #Flight number value
                    self.data['Flight No.'].append(flight_number)
                    datetimelist=self.date_time(row[0])
                    
                    #Date Value
                    self.data['Date'].append(datetimelist[0])
                    date = datetimelist[0].strip(',')
                    
                    #Time Value
                    self.data['Time'].append(datetimelist[1])
                    time = datetimelist[1]
                    
                    #Booster version
                    bv = self.booster_version(row[1])
                    if not(bv):
                        bv=row[1].a.string
                    self.data['Version Booster'].append(bv)
                    
                    #launch Site
                    launch_site = row[2].a.string
                    self.data['Launch site'].append(launch_site)
                    
                    #Payload
                    payload = row[3].a.string
                    self.data['Payload'].append(payload)
                    
                    #Payload Mass
                    payload_mass = self.get_mass(row[4])
                    self.data['Payload mass'].append(payload_mass)
                    
                    #Orbit
                    orbit = row[5].a.string
                    self.data['Orbit'].append(orbit)
                    
                    #Customer
                    customer = None
                    if row[6].a:
                        customer = row[6].a.string
                    else:
                        customer = row[6].string
                    self.data['Customer'].append(customer)
                    
                    #Launch outcome
                    launch_outcome = list(row[7].strings)[0]
                    self.data['Launch outcome'].append(launch_outcome)
                    
                    #Booster Landing
                    booster_landing = self.landing_status(row[8])
                    self.data['Booster landing'].append(booster_landing)
                    
                    self.webscrape_df = pd.DataFrame(self.data)
                    
