import requests
import json
import os
import configparser
import pandas as pd
from datetime import datetime as dt
import os
import io
import configparser
from sqlalchemy import create_engine

engine=create_engine("postgresql+psycopg2://weather:abc123@localhost:5432/weather")

def load_to_database():

    df = pd.read_csv('formated_data.csv')
    df.to_sql('weather_forecast', engine, if_exists= 'replace', index= False)
    engine.dispose()

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")

# Fetches the api key from your config.ini file
API_KEY = config.get("DEV", "API_KEY")


WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast?"

cnt = 40

geo_locations = {
    "Harrare": (-17.824858, 31.053028),
    "Kiev": (50.450001, 30.523333),
    "Hokuto": (35.84, 138.40),
    "Melbourne": (-37.83, 144.87),
    "Vitoria": (-20.3194, -40.3378),
    "Konstanz": (47.6603, 9.1758),
    "Crown Point": (41.416981, -87.365314)
}

def save_file(path, data):
    file = io.open(path, "w")
    file.write(str(data))
    file.close()

def load_weather_data():
    # For every city, fetch and store weather data
    json_list = []
    for city in geo_locations:

        (lat, lon) = geo_locations[city]

        # The parameters for the REST API call
        params = {
            "lat": lat,
            "lon": lon,
            "cnt": cnt,
            "appid": API_KEY
        }

        # Fetching the data using HTTP method GET
        # URL using the params parameter will become:
        #   https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&appid=<your_key>
        response = requests.get(WEATHER_URL, params=params)

        if response.status_code == 200:  # If connection is successful (200: http ok)
            raw_data = response.json()  # Get raw data
            json_list.append(raw_data)
            
    json_data = json.dumps(json_list)  
    save_file(CURR_DIR_PATH + "/raw_json_data.json", json_data) 
       

def harmonize_weather_data():
    data_list = []
    
    json_file = open("raw_json_data.json", 'r')
    loaded_data = json.load(json_file)
    
    for data in loaded_data:
        for item in data['list']:
            weather_data = {
                "Date": dt.fromtimestamp(item["dt"]).strftime("%Y-%m-%d"),
                "Temperature": round(item["main"]['temp'] - 273, 2),
                "Air Pressure": item["main"]['pressure'],
                "Weather Description": item["weather"][0]['description'],
                "Clouds": item["clouds"]["all"],
                "City": data["city"]["name"]
            }
            data_list.append(weather_data)
            
    json_file.close()
    harmonized_data = json.dumps(data_list)    
    save_file(CURR_DIR_PATH + "/harmonized_json_data.json", harmonized_data) 
    
    
def transform_harmonized_to_data_frame():
    json_file = open("harmonized_json_data.json", 'r')
    harmonized_data = json.load(json_file)
    df = pd.DataFrame.from_dict(harmonized_data)
    
    df.to_csv("formated_data.csv",index=False)

if __name__ == "__main__":
    #load_weather_data()
    #harmonize_weather_data()
    #transform_harmonized_to_data_frame()
    load_to_database()
