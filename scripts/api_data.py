import requests
import pandas as pd
import numpy as np
import datetime

spacex_url='https://api.spacexdata.com/v4/launches/past'

response = requests.get(spacex_url)
print(response.content)