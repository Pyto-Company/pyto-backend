from dataclasses import dataclass
from typing import Optional

@dataclass
class WeatherData:
    time: str
    cloudBase: Optional[float]
    cloudCeiling: Optional[float]
    cloudCover: int
    dewPoint: float
    freezingRainIntensity: int
    humidity: int
    precipitationProbability: int
    pressureSurfaceLevel: float
    rainIntensity: int
    sleetIntensity: int
    snowIntensity: int
    temperature: float
    temperatureApparent: float
    uvHealthConcern: int
    uvIndex: int
    visibility: float
    weatherCode: int
    windDirection: float
    windGust: float
    windSpeed: float

@dataclass
class Location:
    lat: float
    lon: float
    name: str
    type: str

@dataclass
class WeatherReport:
    data: WeatherData
    location: Location
