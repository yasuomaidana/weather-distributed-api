from tqdm import tqdm
from weather_api_caller.countries.country_finder import get_all_countries, find_country
from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from weather_api_caller.weather_api.WeatherApi import WeatherApi
from datetime import datetime, timedelta


def get_today() -> datetime:
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    return datetime.strptime(date, '%Y-%m-%d %H:%M')


def get_tomorrow(date: datetime = get_today()):
    one_day = timedelta(days=1)
    return date + one_day


def get_yesterday(date: datetime = get_today()):
    one_day = timedelta(days=1)
    return date - one_day


class WeatherCaller:
    def __init__(self, configuration: str):
        self.mongo_db = MongoDataBase(configuration)
        self.api = WeatherApi(configuration)

    def update_all_weathers(self, date: datetime = get_today()):
        print("Updating weather information")
        for short_name, coordinate in tqdm(get_all_countries()):
            country = find_country(short_name)
            if self.mongo_db.get_existing_weather(date, country.city_name):
                continue
            if self.mongo_db.get_existing_weather(date, country.short_name, key='short_name'):
                continue

            weathers = self.api.call_api(country.coordinate, country)

            if weathers:
                self.mongo_db.insert_weather(weathers)

    def get_similar_weather(self, place: str, date=get_today()) -> list[WeatherData]:

        data = self.get_weather(place, date)
        if data is None:
            self.mongo_db.delete_old_weather(date)
            self.update_all_weathers(date)
            data = self.get_weather(place, date)
        similar_weather = self.mongo_db.get_similar_weathers(date, data.weather_status)
        return similar_weather

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
