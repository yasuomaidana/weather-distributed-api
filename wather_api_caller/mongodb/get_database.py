from typing import List, Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from datetime import datetime

from wather_api_caller.configuration.Configuration import Configuration
from wather_api_caller.data.WeatherData import WeatherData


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


if __name__ == "__main__":
    db_config = Configuration("config_database_test").get_database()
    database = get_database(db_config)
    test_collection = define_collection(database, db_config)
    test_collection.drop()
    weather0 = WeatherData("Beijing", "CNs", "Partly cloudy", 36.5, 80, '2023-07-24')
    weather1 = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80, '2023-07-24')
    weather2 = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80, '2023-07-25')
    weather3 = WeatherData("Beijing", "CN", "Partly cloudy", 36.5, 80, '2023-07-26')
    print([weather0, weather1, weather2, weather3])
    insert_data(test_collection, [weather1, weather2, weather3])
    print("---All---")
    [print(i) for i in get_weather_data(test_collection)]
    print("2023-07-25")
    print(get_weather_by_date(test_collection, datetime.strptime("2023-07-25", '%Y-%m-%d')))
    print("2023-07-28")
    print(get_weather_by_date(test_collection, datetime.strptime("2023-07-28", '%Y-%m-%d')))
    print("Removing Dates before 2023-07-25")
    print(delete_weather_data_before_date(test_collection, datetime.strptime("2023-07-25", '%Y-%m-%d')))
    print("---All after removing---")
    [print(i) for i in get_weather_data(test_collection)]
    print("Today")
    print(datetime.today().date())
