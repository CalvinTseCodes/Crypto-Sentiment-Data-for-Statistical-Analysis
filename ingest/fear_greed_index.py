import requests
import json
from datetime import datetime

#API request for 365 days of fear greed index data in json file format
url = "https://api.alternative.me/fng/"
params = {"limit": 365, "format": "json"}
response = requests.get(url, params=params)

#Takes json file response and converts into a python-readable data structures
data = response.json()

#Use datetime to mark when I ran the file and makes sure I didn't overwrite the old one
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/alternative/fg_index_{ts}.json"

#Saves the data as a json file while adding line breaks for readability
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")
