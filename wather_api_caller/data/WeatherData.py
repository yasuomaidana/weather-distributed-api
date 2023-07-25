from datetime import datetime


class WeatherData:
    def __init__(self, name: str, short_name: str, weather_status: str, temperature: float, humidity: float,
                 date: str):
        self.name = name
        self.short_name = short_name
        self.weather_status = weather_status
        self.temperature = temperature
        self.humidity = humidity
        self.date = datetime.strptime(date, '%Y-%m-%d')


if __name__ == "__main__":
    weather = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80, "2023-07-25")
    print(vars(weather))
