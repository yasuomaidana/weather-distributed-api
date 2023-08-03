import requests

from weather_api_caller.configuration.Configuration import Configuration
from weather_api_caller.countries.country_finder import find_country
from weather_api_caller.data.WeatherData import WeatherData
from datetime import datetime

def handle_call():
    pass
class WeatherApi:
    def __init__(self, configuration_yaml: str):
        config = Configuration(configuration_yaml).get_api()
        self.endpoint = "https://" + config["host"] + config["request"]
        self.header = {
            'X-RapidAPI-Key': config["key"],
            'X-RapidAPI-Host': config["host"]
        }

    def call_api(self, query):
        res = requests.get(self.endpoint, headers=self.header, params=query)
        if not res.ok:
            return None
        data = res.json()
        forecast = data["forecast"]
        place_weather = []
        country = find_country(data["location"]["country"])
        if country is None:
            for i in data["location"]["country"].split():
                country = find_country(i)
                if country:
                    break
            if country is None:
                country = data["location"]["country"]
                letters = [word[0].upper() for word in country]
                country = ''.join(letters)

        for day in forecast["forecastday"]:
            for hour in day["hour"]:
                date = hour["time"]
                date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                temp = hour["temp_c"]
                status = hour["condition"]["text"]
                humidity = hour["humidity"]
                weather = WeatherData(data["location"]["name"], data["location"]["country"], country.short_name, status,
                                      temp, humidity, date)
                place_weather.append(weather)
        return place_weather

    def get_country_weather(self, place: str) -> list[WeatherData] | None:
        country = find_country(place)
        if country is None:
            return None
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
