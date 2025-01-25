import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
from app.dto.PrevisionMeteoDTO import PrevisionMeteoDTO

# Charger les variables d'environnement
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

# https://openweathermap.org/current
CURREN_WEATHER_API="https://api.openweathermap.org/data/2.5/weather"
# https://openweathermap.org/forecast5
FIVE_DAYS_FORECAST_API="https://api.openweathermap.org/data/2.5/forecast"
# https://openweathermap.org/api/air-pollution
CURRENT_AIR_POLLUTION_API="http://api.openweathermap.org/data/2.5/air_pollution"

class OpenWeatherClient():

    def get_weather(lat: float, lon: float):
        """
        Récupère les données météo pour une ville donnée.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPEN_WEATHER_API_KEY,
            "units": "metric",  # Pour des données en Celsius
            "lang": "fr"        # Langue française pour les descriptions
        }
        
        response = requests.get(CURREN_WEATHER_API, params=params)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des données météo")
        
        data = response.json()
        
        # Extraire les informations clés
        weather_data = {
            "ville": data.get("name"),
            "temperature": data["main"].get("temp"),
            "description": data["weather"][0].get("description"),
            "vent": data["wind"].get("speed"),
            "humidite": data["main"].get("humidity"),
        }
        
        return weather_data

    def get_forecast(lat: float, lon: float):
        """
        Récupère les prévisions météo pour une ville donnée.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPEN_WEATHER_API_KEY,
            "units": "metric",  # Pour des données en Celsius
            "lang": "fr"        # Langue française pour les descriptions
        }
        

        response = requests.get(FIVE_DAYS_FORECAST_API, params=params)
            
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des données météo")
        
        data = response.json()
        
        # Extraire les informations clés
        forecast = []
        for row in data.get("list"):

            # Conversion du timestamp epoch en date
            epoch_time = row.get("dt")
            forecast_date = datetime.fromtimestamp(epoch_time).date()

            prevision = PrevisionMeteoDTO(
                date=forecast_date,
                temperature=row.get("main").get("temp"),
                meteo=row.get("weather")[0].get("main"),
            )
            forecast.append(prevision)

        return forecast


    def get_pollution(lat: float, lon: float):
        """
        Récupère les données pollution pour une ville donnée.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPEN_WEATHER_API_KEY
        }
        
        response = requests.get(CURRENT_AIR_POLLUTION_API, params=params)
            
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des données météo")
        
        return response
