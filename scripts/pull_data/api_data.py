import requests
import pandas as pd
from datetime import date
from pathlib import Path

spacex_url='https://api.spacexdata.com/v4/launches/past'



class API_call:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.cleaned_df = None
        
    def fetch_api(self):
        response = requests.get(self.url)
        data = response.json()
        self.data = pd.json_normalize(data)
    
    # Flatten out api core values             
    def getCoreData(self, data):
        for core in data['cores']:
                if core['core'] != None:
                    response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                    self.cleaned_df['Block'].append(response['block'])
                    self.cleaned_df['ReusedCount'].append(response['reuse_count'])
                    self.cleaned_df['Serial'].append(response['serial'])
                else:
                    self.cleaned_df['Block'].append(None)
                    self.cleaned_df['ReusedCount'].append(None)
                    self.cleaned_df['Serial'].append(None)
                self.cleaned_df['Flights'].append(core['flight'])
                self.cleaned_df['GridFins'].append(core['gridfins'])
                self.cleaned_df['Reused'].append(core['reused'])
                self.cleaned_df['Legs'].append(core['legs'])
                self.cleaned_df['LandingPad_ID'].append(core['landpad'])
                
   # Get landing pad data             
    def getLandingPad(self, ids):
        for id in ids:
            if id == None:
                self.cleaned_df['LandingPad'].append(None)
            else:
                response = requests.get(f"https://api.spacexdata.com/v4/landpads/{id}").json()
                self.cleaned_df['LandingPad'].append(response['name'])
                
    # Filters launch data to include only records with a single core and single payload                      
    def filter_data(self):
        data = self.data
        data = data[['payloads','cores', 'flight_number', 'date_utc']]
        # Converts lists (cores and payloads) into single dictionary entries
        data = data[data['cores'].map(len)==1]
        data = data[data['payloads'].map(len)==1]
        # Only applies to non-empty lists
        data['cores'] = data['cores'].map(lambda x: x[0] if x else None)
        
        self.cleaned_df = {}
        self.cleaned_df['Flight_number'] = data['flight_number']
        self.cleaned_df['Flights'] = []
        self.cleaned_df['GridFins'] = []      
        self.cleaned_df['Reused'] = []
        self.cleaned_df['Legs'] = []
        self.cleaned_df['LandingPad_ID'] = []
        self.cleaned_df['LandingPad'] = []
        self.cleaned_df['Block'] = []
        self.cleaned_df['ReusedCount'] = []
        self.cleaned_df['Serial'] = []
        self.cleaned_df['Date'] = data['date_utc']
        
        self.getCoreData(data)
        self.getLandingPad(self.cleaned_df['LandingPad_ID'])
        
        del self.cleaned_df['LandingPad_ID']
        
        self.cleaned_df = pd.DataFrame.from_dict(self.cleaned_df)
     
    # Saves cleaned DataFrame as a timestamped CSV in the 'data/raw_data' folder   
    def save_data(self):
        root_dir = Path(__file__).resolve().parent.parent.parent
        raw_data_path = root_dir/'data'/'raw_data'
        raw_data_path.mkdir(parents=True, exist_ok=True)

        today = date.today().strftime("%Y_%m_%d")

        csv_path = raw_data_path/f'spaceX_api_data_{today}.csv'

        self.cleaned_df.to_csv(csv_path, index=False)
            
    # Executes full pipeline: fetch, clean, and save SpaceX launch data to CSV   
    def pull_save_data(self):
        self.fetch_api()
        self.filter_data()
        self.save_data()



api_data = API_call(spacex_url)
api_data.pull_save_data()

