from time_manager import TimeManager
from weather_manager import WeatherManager
from terminal import Terminal


def main():
    # Replace with your API key
    api_key = "YOUR_API_KEY_HERE"

    # Create instances of TimeManager and WeatherManager
    time_manager = TimeManager()
    weather_manager = WeatherManager(api_key)

    # Get city name from user
    city = Terminal.ask_for_city()

    weather_details = weather_manager.get_weather(city)

    if weather_details:
        temperature, pressure, humidity, weather_description = weather_details
        current_time = time_manager.get_current_time()

        Terminal.display_time_and_weather(
            current_time, city, temperature, pressure, humidity, weather_description
        )
    else:
        Terminal.display_error("City not found!")


if __name__ == "__main__":
    main()
