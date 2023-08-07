class Terminal:
    @staticmethod
    def ask_for_city():
        return input("Enter city name: ")

    @staticmethod
    def display_time_and_weather(
        time, city, temperature, pressure, humidity, description
    ):
        print("Current Time:", time)
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature:.2f}°C")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")

    @staticmethod
    def display_error(message):
        print(message)
