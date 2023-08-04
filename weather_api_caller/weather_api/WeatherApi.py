import requests
from requests import Response

from weather_api_caller.configuration.Configuration import Configuration
from weather_api_caller.countries.country_finder import find_country, CountryName
from weather_api_caller.data.WeatherData import WeatherData
from datetime import datetime
from difflib import SequenceMatcher

from weather_api_caller.time_utilery.time_builders import convert_to_local


def handle_find_country(location, fixed: WeatherData = None):
    if fixed:
        return fixed
    name = location["name"]
    country_by_name = None if location["name"] == "" else find_country(location["name"])
    country_by_region = None if location["region"] == "" else find_country(location["region"])
    country_by_country = find_country(location["country"])

    country = None
    if country_by_country:
        country = country_by_country

    elif country_by_name:
        country = country_by_name

    elif country_by_region:
        country = country_by_region

    if country:
        ratio = SequenceMatcher(None, name, country.city_name).ratio()
        city_name = country.city_name if ratio < 0.8 else name
        country._replace(city_name=city_name)
    return country


def handle_call(response: Response, fixed: CountryName = None) -> CountryName:
    if response.ok:
        data = response.json()

        country = handle_find_country(data["location"], fixed)

        if country is None:
            for i in data["location"]["country"].split():
                country = find_country(i)
                if country:
                    return country
            if country is None:
                country = data["location"]["country"]
                letters = [word[0].upper() for word in country]
                country = ''.join(letters)
                country = CountryName(city_name=data["location"]["name"], short_name=country,
                                      country=data["location"]["country"], coordinate="")
        return country


class WeatherApi:
    def __init__(self, configuration_yaml: str):
        config = Configuration(configuration_yaml).get_api()
        self.endpoint = "https://" + config["host"] + config["request"]
        self.header = {
            'X-RapidAPI-Key': config["key"],
            'X-RapidAPI-Host': config["host"]
        }

    def call_api(self, query, fixed: CountryName = None):
        if isinstance(query, str):
            query = {"q": query, "days": "1"}
        res = requests.get(self.endpoint, headers=self.header, params=query)
        country = handle_call(res, fixed)
        if not country:
            return None
        data = res.json()
        forecast = data["forecast"]
        place_weather = []

        for day in forecast["forecastday"]:
            for hour in day["hour"]:
                date = hour["time_epoch"]
                date = convert_to_local(date)
                temp = hour["temp_c"]
                status = hour["condition"]["text"]
                humidity = hour["humidity"]
                weather = WeatherData(country.city_name, country.city_name, country.short_name, status,
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
            date = convert_to_local(date)
            day = day["day"]
            temp = day["avgtemp_c"]
            status = day["condition"]["text"]
            humidity = day["avghumidity"]
            weather = WeatherData(country.city_name, country.country, country.short_name, status, temp, humidity, date)
            place_weather.append(weather)
        return place_weather
