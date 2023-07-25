from typing import List, Union, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from wather_api_caller.configuration.Configuration import Configuration
from wather_api_caller.data.WeatherData import WeatherData


def get_database(config: Configuration) -> Database:
    connection_string = f"mongodb+srv://yasuo_distributed:{password}@weather.lriaphk.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client["Weather"]


def define_collection_unique(db: Database, collection_name: str, prop: Optional[List] = None) -> Collection:
    collection = db[collection_name]
    if prop is not None:
        collection.create_index(prop, unique=True)
    return collection


def insert_data(client: Collection, data: Union[WeatherData, List[WeatherData]]):
    if isinstance(data, WeatherData):
        client.insert_one(vars(data))
    else:
        data = [vars(i) for i in data]
        client.insert_many(data)


def get_weather_data(client: Collection):
    pass


if __name__ == "__main__":
    with open('auth.txt') as f:
        password = f.readline()
    f.close()
    dbname = get_database(password)
    test_collection = define_collection_unique(dbname, "test", ['name', 'short_name'])
    test_collection.drop()
    weather = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80)
    insert_data(test_collection, weather)
