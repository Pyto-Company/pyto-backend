import requests

from dto.weatherData import WeatherData, WeatherReport

class MeteoService():

    def get(location: str) -> WeatherData:
        result = requests.get('https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey=JUx0lyHFlnwuu95W5PBsGDbu15xqQZYq').json()
        weatherData = WeatherReport(**result) 
        return weatherData

