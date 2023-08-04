from weather_api_caller.mongodb.get_database import *
from datetime import datetime, timedelta

from weather_api_caller.configuration.Configuration import Configuration
from weather_api_caller.data.WeatherData import cast_dict_to_weather_data


class MongoDataBase:
    def __init__(self, configuration_yaml: str):
        db_config = Configuration(configuration_yaml).get_database()
        self.database = get_database(db_config)
        self.collection = define_collection(self.database, db_config)

    def insert_weather(self, weather: Union[WeatherData, List[WeatherData]]):
        insert_data(self.collection, weather)

    def get_weather_by_hour_and_place(self, hour: datetime, place: str, place_sel="city_name"):
        date = hour.replace(minute=0, second=0, microsecond=0)
        next_hour = date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        return self.collection.find_one(
            {
                'date': {
                    '$gte': date,
                    '$lt': next_hour
                },
                place_sel: place
            })

    def get_weather_by_date_and_place(self, date: datetime, place: str, place_sel="city_name"):

        single_weather = self.get_weather_by_hour_and_place(date, place, place_sel)

        if single_weather:
            return cast_dict_to_weather_data(dict(single_weather))
        return None

    def get_existing_weather(self, date: datetime, place: str, key='city_name') -> WeatherData | None:
        date = date.replace(minute=0, second=0, microsecond=0)
        next_hour = date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        weather = self.collection.find_one(
            {
                'date': {
                    '$lt': next_hour
                },
                key: place
            })
        if weather:
            return cast_dict_to_weather_data(dict(weather))
        else:
            return None

    def get_similar_weathers(self, date: datetime, weather_status: str):
        # Calculate the next exact hour
        date = date.replace(minute=0, second=0, microsecond=0)
        next_hour = date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        weathers = self.collection.find(
            {
                'date': {
                    '$gte': date,
                    '$lt': next_hour
                },
                'weather_status': weather_status
            })
        return [cast_dict_to_weather_data(i) for i in weathers]

    def get_weather_by_date(self, date: datetime):
        return [cast_dict_to_weather_data(i) for i in get_weather_by_date(self.collection, date)]

    def delete_old_weather(self, date: datetime):
        delete_weather_data_before_date(self.collection, date)

    def clean(self):
        self.collection.drop()
