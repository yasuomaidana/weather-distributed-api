class WeatherData:
    def __init__(self, name: str, short_name: str, weather_status: str, temperature: float, humidity: float):
        self.name = name
        self.short_name = short_name
        self.weather_status = weather_status
        self.temperature = temperature
        self.humidity = humidity


if __name__ == "__main__":
    weather = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80)
    print(vars(weather))
