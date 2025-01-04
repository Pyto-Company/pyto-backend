from fastapi import APIRouter, HTTPException, Query
from app.client.open_weather import OpenWeatherClient
from app.service.meteo import MeteoService

router = APIRouter(prefix="/meteo", tags=["meteo"])

@router.post("/")
async def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)}

""" @router.get("/{id}")
async def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)} """

@router.get("/realtime")
async def realtime(location: str):
    weatherData = MeteoService.get(location)
    return {"weatherData": str(weatherData)}

@router.get("/weather")
async def get_weather(lat: float, lon: float):
    return await OpenWeatherClient.get_weather(lat, lon)

@router.get("/forecast")
async def get_forecast(lat: float, lon: float):
    return await OpenWeatherClient.get_forecast(lat, lon)

@router.get("/pollution")
async def get_pollution(lat: float, lon: float):
    return await OpenWeatherClient.get_pollution(lat, lon)