import requests
import pandas as pd

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
        
        
        
    def getBoosterVersion(self, data):
        for x in data['rocket']:
            if x:
                response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
                self.cleaned_df['BoosterVersion'].append(response['name'])
                
    def getLaunchSite(self, data):
        for x in data['launchpad']:
            if x:
                
                response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
                self.cleaned_df['Longitude'].append(response['longitude'])
                self.cleaned_df['Latitude'].append(response['latitude'])
                self.cleaned_df['LaunchSite'].append(response['name'])
         
    def getPayloadData(self, data):
        for load in data['payloads']:
            if load:
                response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
                self.cleaned_df['PayloadMass'].append(response['mass_kg'])
                self.cleaned_df['Orbit'].append(response['orbit'])
                
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
                if core['landpad'] != None:
                    response = requests.get("https://api.spacexdata.com/v4/landpads/"+core['landpad']).json()
                    self.cleaned_df['LandingPad'].append(response['name'])
                else:
                    self.cleaned_df['LandingPad'].append(None)
                self.cleaned_df['Outcome'].append(str(core['landing_success'])+' '+str(core['landing_type']))
                self.cleaned_df['Flights'].append(core['flight'])
                self.cleaned_df['GridFins'].append(core['gridfins'])
                self.cleaned_df['Reused'].append(core['reused'])
                self.cleaned_df['Legs'].append(core['legs'])
                    
                
    
        
    def filter_data(self):
        data = self.data
        data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
        #filtering out all rockets with muliple payloads and rocket boosters to make the data more uniform
        data = data[data['cores'].map(len)==1]
        data = data[data['payloads'].map(len)==1]
        #coverting from list to single value and making sure list is not empty
        data['cores'] = data['cores'].map(lambda x: x[0] if x else None)
        data['payloads'] = data['payloads'].map(lambda x: x[0] if x else None)
        
        data['date'] = pd.to_datetime(data['date_utc']).dt.date
        
        self.cleaned_df = {}
        
        self.cleaned_df['Flight_number'] = data['flight_number']
        self.cleaned_df['BoosterVersion'] = []
        self.cleaned_df['PayloadMass'] = []
        self.cleaned_df['Orbit'] = []
        self.cleaned_df['LaunchSite'] = []
        self.cleaned_df['Outcome'] = []
        self.cleaned_df['Flights'] = []
        self.cleaned_df['GridFins'] = []
        self.cleaned_df['Reused'] = []
        self.cleaned_df['Legs'] = []
        self.cleaned_df['LandingPad'] = []
        self.cleaned_df['Block'] = []
        self.cleaned_df['ReusedCount'] = []
        self.cleaned_df['Serial'] = []
        self.cleaned_df['Longitude'] = []
        self.cleaned_df['Latitude'] = []
        self.cleaned_df['Date'] = data['date']
        
        self.getBoosterVersion(data)
        
        self.getLaunchSite(data)
        
        self.getPayloadData(data)
        
        self.getCoreData(data)
        
        self.cleaned_df = pd.DataFrame.from_dict(self.cleaned_df)
        