import requests
import json
from datetime import datetime

#API request for a whole year of daily Bitcoin data
url = "https://api.binance.com/api/v3/klines"
params = {"symbol": "BTCUSDT", "interval": "1d", "limit": 365}
response = requests.get(url, params=params)

#Checks if request was successful
response.raise_for_status()

#Takes json file response and converts into a python-readable data structures
data = response.json()

#Use datetime to mark when I ran the file and makes sure I didn't overwrite the old one
ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
filename = f"data/bronze/binance/btc_klines_{ts}.json"

#Saves the data as a json file while adding line breaks for readability
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {filename}")