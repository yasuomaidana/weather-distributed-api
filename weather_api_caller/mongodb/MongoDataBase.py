from get_database import *
from datetime import datetime

from wather_api_caller.configuration.Configuration import Configuration
from wather_api_caller.data.WeatherData import cast_dict_to_weather_data


class MongoDataBase:
    def __init__(self, configuration_yaml: str):
        db_config = Configuration(configuration_yaml).get_database()
        self.database = get_database(db_config)
        self.collection = define_collection(self.database, db_config)

    def insert_weather(self, weather: Union[WeatherData, List[WeatherData]]):
        insert_data(self.collection, weather)

    def get_weather_by_date(self, date: datetime):
        return [cast_dict_to_weather_data(i) for i in get_weather_by_date(self.collection, date)]

    def delete_old_weather(self, date: datetime):
        delete_weather_data_before_date(self.collection, date)
