import sys
sys.path.insert(0, r'C:\Users\rossm\Data_Science_Work\SpaceX_DataProject\data')
import pandas as pd
import numpy as np
from raw_data import scraped_df, api_df

api_df = api_df[['Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial', 'Longitude', 'Latitude', 'Date']]

scraped_df['Date'] = pd.to_datetime(scraped_df['Date'], errors='coerce').dt.date

api_df['Date'] = pd.to_datetime(api_df['Date'], errors='coerce').dt.date

merged_df = scraped_df.merge(api_df, on='Date', how='left', suffixes=('','_api'))
merged_df

merged_df1 = merged_df.dropna(subset=['GridFins']).copy()

merged_df1['Booster landing'] = merged_df1['Booster landing'].str.strip()
merged_df1 = merged_df1[~merged_df1['Booster landing'].isin(['No attempt','Uncontrolled'])].copy()


merged_df1.loc[44,'LandingPad'] = 'LZ-4'
merged_df1.loc[merged_df1['LandingPad'].isna(), 'LandingPad'] = 'LZ-1'


spacex_df = merged_df1.rename(columns={'Flight No.': 'Flight #', 'Version Booster': 'Version booster', 'GridFins': 'Grid Fins', 'LandingPad': 'Landing Pad', 'ReusedCount': 'ReusedCount'}).copy()

print(spacex_df)



