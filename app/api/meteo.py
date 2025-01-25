from fastapi import APIRouter, HTTPException, Query
from app.client.open_weather import OpenWeatherClient
from app.service.meteo import MeteoService

router = APIRouter(prefix="/meteo", tags=["meteo"])

@router.post("/")
def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)}

""" @router.get("/{id}")
def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)} """

@router.get("/realtime")
def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)}

@router.get("/weather")
def get_weather(lat: float, lon: float):
    return OpenWeatherClient.get_weather(lat, lon)

@router.get("/previsions")
def get_forecast(lat: float, lon: float):
    return OpenWeatherClient.get_forecast(lat, lon)

@router.get("/pollution")
def get_pollution(lat: float, lon: float):
    return OpenWeatherClient.get_pollution(lat, lon)