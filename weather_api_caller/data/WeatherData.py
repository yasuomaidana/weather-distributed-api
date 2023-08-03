from datetime import datetime
from typing import Union


def cast_dict_to_weather_data(data: dict) -> 'WeatherData':
    data.pop("_id")
    return WeatherData(**data)


class WeatherData:
    def __init__(self, city_name: str, country_name: str, short_name: str, weather_status: str, temperature: float,
                 humidity: float, date: Union[str, datetime]):

        self.city_name = city_name
        self.country_name = country_name
        self.short_name = short_name
        self.weather_status = weather_status
        self.temperature = temperature
        self.humidity = humidity
        if isinstance(date, str):
            self.date = datetime.strptime(date, '%Y-%m-%d %H:%M')
        else:
            self.date = date
