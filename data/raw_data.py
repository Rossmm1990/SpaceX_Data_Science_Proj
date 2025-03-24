import sys
sys.path.insert(0, r'C:\Users\rossm\Data_Science_Work\SpaceX_DataProject\scripts')
from web_scraping import WebScraper
from api_data import API_call



web_scrape_data = WebScraper("https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922")
web_scrape_data.fetch_data()
web_scrape_data.extract_data()

api_call_data = API_call('https://api.spacexdata.com/v4/launches/past')
api_call_data.fetch_api()
api_call_data.filter_data()

scraped_df = web_scrape_data.webscrape_df
api_df = api_call_data.cleaned_df


