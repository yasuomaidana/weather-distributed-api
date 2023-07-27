from weather_api_caller.countries.country_finder import get_all_countries, find_country
from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from weather_api_caller.weather_api.WeatherApi import WeatherApi
from datetime import datetime


def get_today() -> datetime:
    date = datetime.today().strftime('%Y-%m-%d')
    return datetime.strptime(date, '%Y-%m-%d')


class WeatherCaller:
    def __init__(self, configuration: str):
        self.mongo_db = MongoDataBase(configuration)
        self.api = WeatherApi(configuration)

    def update_all_weathers(self, date: datetime = get_today()):
        for short_name, coordinate in get_all_countries():
            if self.mongo_db.get_existing_weather(date, short_name):
                continue
            weathers = self.api.get_country_weather(short_name)
            if weathers:
                self.mongo_db.insert_weather(weathers)

    def get_similar_weather(self, shortname: str, date=get_today()) -> list[WeatherData]:
        data = self.get_weather(shortname, date)
        if data is None:
            self.mongo_db.delete_old_weather(date)
            self.update_all_weathers(date)
            data = self.mongo_db.get_weather_by_date_and_place(date, find_country(shortname).short_name)
        similar_weather = self.mongo_db.get_similar_weathers(date, data.weather_status)
        return similar_weather

    def get_weather(self, shortname: str, date=get_today()) -> WeatherData:
        return self.mongo_db.get_weather_by_date_and_place(date, find_country(shortname).short_name)
