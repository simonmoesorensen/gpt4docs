import requests


class WeatherManager:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "q=" + city + "&appid=" + self.api_key
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            return self._format_weather_response(weather_data)

    def _format_weather_response(self, weather_data):
        main_data = weather_data["main"]
        weather = weather_data["weather"]
        temperature = main_data["temp"] - 273.15  # Convert from Kelvin to Celsius
        pressure = main_data["pressure"]
        humidity = main_data["humidity"]
        weather_description = weather[0]["description"]

        return temperature, pressure, humidity, weather_description
