from scripts.web_scraping.py import WebScraper

web_scrape_data = WebScraper("https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922")
web_scrape_data.fetch_data()
web_scrape_data.extract_data()

scraped_data = web_scrape_data.data
print(scraped_data)