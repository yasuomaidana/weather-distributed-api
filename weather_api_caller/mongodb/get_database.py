from typing import List, Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from datetime import datetime

from weather_api_caller.data.WeatherData import WeatherData


def get_database(database_config: dict) -> Database:
    dbname = database_config["name"]
    client = MongoClient(database_config["connection_string"])
    return client[dbname]


def define_collection(db: Database, config: dict) -> Collection:
    collection = db[config["collection"]]
    collection.create_index(config["unique"], unique=True)
    return collection


def insert_data(client: Collection, data: Union[WeatherData, List[WeatherData]]):
    if isinstance(data, WeatherData):
        client.insert_one(vars(data))
    else:
        data = [vars(i) for i in data]
        client.insert_many(data)


def get_weather_by_date(collection: Collection, date: datetime):
    query = {'date': date}
    return list(collection.find(query))


def delete_weather_data_before_date(collection: Collection, date: datetime):
    query = {'date': {"$lt": date}}
    collection.delete_many(query)


def get_weather_data(client: Collection):
    return client.find()

