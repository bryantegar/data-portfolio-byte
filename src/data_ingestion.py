import json
import requests
import pandas as pd
from datetime import datetime
import os

# Load config
with open("config.json", "r") as file:
    config = json.load(file)

# Extract config values
API_URL = config["data_source"]["API_URL"]
latitude = config["data_source"]["latitude"]
longitude = config["data_source"]["longitude"]

params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": ",".join(config["data_source"]["parameters"])
}

# Fetch data from API
response = requests.get(API_URL, params=params)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data["hourly"])
df["timestamp"] = pd.to_datetime(df["time"])

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Save file with timestamp name
filename = f"data/weather_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv"
df.to_csv(filename, index=False)

print(f"Data saved successfully → {filename}")
