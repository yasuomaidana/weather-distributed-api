from pymongo.errors import DuplicateKeyError

from weather_api_caller.mongodb.get_database import *
from datetime import datetime

from weather_api_caller.configuration.Configuration import Configuration
from weather_api_caller.data.WeatherData import cast_dict_to_weather_data


class MongoDataBase:
    def __init__(self, configuration_yaml: str):
        db_config = Configuration(configuration_yaml).get_database()
        self.database = get_database(db_config)
        self.collection = define_collection(self.database, db_config)

    def insert_weather(self, weather: Union[WeatherData, List[WeatherData]]):
        insert_data(self.collection, weather)

    def get_weather_by_date_and_place(self, date: datetime, shortname: str):
        single_weather = self.collection.find_one({'date': date, 'short_name': shortname})
        if single_weather:
            return cast_dict_to_weather_data(dict(single_weather))
        return None

    def get_existing_weather(self, date: datetime, shortname: str) -> WeatherData | None:
        weather = self.collection.find_one({'date': {"$gte": date}, 'short_name': shortname})
        if weather:
            return cast_dict_to_weather_data(dict(weather))
        else:
            return None

    def get_similar_weathers(self, date: datetime, weather_status: str):
        weathers = self.collection.find({'date': date, 'weather_status': weather_status})
        return [cast_dict_to_weather_data(i) for i in weathers]

    def get_weather_by_date(self, date: datetime):
        return [cast_dict_to_weather_data(i) for i in get_weather_by_date(self.collection, date)]

    def delete_old_weather(self, date: datetime):
        delete_weather_data_before_date(self.collection, date)

    def clean(self):
        self.collection.drop()
