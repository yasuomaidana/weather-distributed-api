from weather_api_caller.countries.country_finder import get_all_countries
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from weather_api_caller.weather_api.WeatherApi import WeatherApi
from datetime import datetime, timedelta


class WeatherCaller:
    def __init__(self, configuration: str):
        self.mongo_db = MongoDataBase(configuration)
        self.api = WeatherApi(configuration)

    def get_weather(self):
        date = datetime.today().strftime('%Y-%m-%d')

        date = datetime.strptime(date, '%Y-%m-%d')
        data = self.mongo_db.get_weather_by_date(date)
        if len(data) == 0:
            self.mongo_db.delete_old_weather(date)
            for city, coordinate in get_all_countries():
                if self.mongo_db.get_weather_by_date_and_place(date, city):
                    continue
                tomorrow = datetime.today().strftime('%Y-%m-%d')
                tomorrow = datetime.strptime(tomorrow, '%Y-%m-%d') + timedelta(days=1)
                if self.mongo_db.get_weather_by_date_and_place(tomorrow, city):
                    continue
                weathers = self.api.get_country_weather(city)
                self.mongo_db.insert_weather(weathers)

        if len(data) != 198:
            pass
        return data
