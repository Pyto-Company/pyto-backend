from app.service.meteo import TomorrowExternalService

def test() -> None:
    weatherData = TomorrowExternalService.get('42.3478,-71.0466')
    print(weatherData)

