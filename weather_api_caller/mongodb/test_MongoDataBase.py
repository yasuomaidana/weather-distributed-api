from unittest import TestCase

from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from datetime import datetime


def toDate(date: str):
    return datetime.strptime(date, '%Y-%m-%d')


class TestMongoDataBase(TestCase):
    mongoDb = MongoDataBase("config_database_test")

    def setUp(self):
        self.mongoDb.collection.drop()
        weather0 = WeatherData("Beijing", "", "CNs", "Partly cloudy", 36.5, 80, '2023-07-24')
        weather1 = WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-24')
        weather2 = WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-25')
        weather3 = WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-26')
        self.mongoDb.insert_weather([weather0, weather1, weather2, weather3])

    @classmethod
    def tearDownClass(cls):
        cls.mongoDb.clean()

    def test_get_weather_by_date(self):
        d24 = self.mongoDb.get_weather_by_date(toDate('2023-07-24'))
        self.assertIsInstance(d24[0], WeatherData)
        self.assertEqual(len(d24), 2)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-25'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-28'))), 0)

    def test_delete_old_weather(self):
        self.mongoDb.delete_old_weather(toDate("2023-07-25"))
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-24'))), 0)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-25'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-26'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-28'))), 0)
