from tqdm import tqdm
from weather_api_caller.countries.country_finder import get_all_countries, find_country
from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from weather_api_caller.time_utilery.time_builders import get_today
from weather_api_caller.weather_api.WeatherApi import WeatherApi
from datetime import datetime


class WeatherCaller:
    def __init__(self, configuration: str):
        self.mongo_db = MongoDataBase(configuration)
        self.api = WeatherApi(configuration)

    def update_all_weathers(self, date: datetime = get_today()):
        print("Updating weather information")
        stored_cities = set(self.mongo_db.get_city_names())
        if len(stored_cities) < 198:
            for short_name, coordinate in tqdm(get_all_countries()):
                country = find_country(short_name)
                if country.city_name in stored_cities:
                    stored_cities.remove(country.city_name)
                if self.mongo_db.get_weather_by_date_and_place(date, country.city_name):
                    continue
                if self.mongo_db.get_weather_by_date_and_place(date, country.short_name, place_sel='short_name'):
                    continue
                weathers = self.api.call_api(country.coordinate, country)
                if weathers:
                    self.mongo_db.insert_weather(weathers)
        else:
            for city_name in tqdm(stored_cities):
                if self.mongo_db.get_weather_by_date_and_place(date, city_name):
                    continue
                weathers = self.api.call_api(city_name)
                if weathers:
                    self.mongo_db.insert_weather(weathers)

    def get_similar_weather(self, place: str, date=get_today()) -> list[WeatherData]:
        self.mongo_db.delete_old_weather(date)
        data = self.get_weather(place, date)
        if data is None:
            self.update_all_weathers(date)
            data = self.get_weather(place, date)
        similar_weather = self.mongo_db.get_similar_weathers(date, data.weather_status)
        return similar_weather

    def check_if_exists(self, name):
        country = find_country(name)
        if country:
            return True
        if self.mongo_db.get_by_similar_name(name):
            return True
        return False

    def get_weather(self, place: str, date=get_today()) -> WeatherData | None:
        country = find_country(place)
        if country:
            return self.mongo_db.get_weather_by_date_and_place(date, country.short_name, "short_name")
        else:
            similar_by_name = self.mongo_db.get_by_similar_name(place)
            if similar_by_name:
                return self.mongo_db.get_weather_by_date_and_place(date, similar_by_name.city_name)
            place_weathers = self.api.call_api(place)
            if place_weathers:
                self.mongo_db.insert_weather(place_weathers)
                return self.mongo_db.get_weather_by_date_and_place(date, place_weathers[0].city_name)
        return None
