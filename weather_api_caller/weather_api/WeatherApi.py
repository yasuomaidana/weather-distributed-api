from typing import List

import requests

from weather_api_caller.configuration.Configuration import Configuration
from weather_api_caller.countries.country_finder import find_country
from weather_api_caller.data.WeatherData import WeatherData
from datetime import datetime


class WeatherApi:
    def __init__(self, configuration_yaml: str):
        config = Configuration(configuration_yaml).get_api()
        self.endpoint = "https://" + config["host"] + config["request"]
        self.header = {
            'X-RapidAPI-Key': config["key"],
            'X-RapidAPI-Host': config["host"]
        }

    def get_country_weather(self, place: str) -> List[WeatherData]:
        country = find_country(place)
        if country is None:
            return []
        query = {"q": country.coordinate, "days": "3"}
        res = requests.get(self.endpoint, headers=self.header, params=query)
        data = res.json()
        forecast = data["forecast"]
        place_weather = []
        for day in forecast["forecastday"]:
            date = day["date"]
            date = datetime.strptime(date, '%Y-%m-%d')
            day = day["day"]
            temp = day["avgtemp_c"]
            status = day["condition"]["text"]
            humidity = day["avghumidity"]
            weather = WeatherData(country.city_name, country.country, country.short_name, status, temp, humidity, date)
            place_weather.append(weather)
        return place_weather
