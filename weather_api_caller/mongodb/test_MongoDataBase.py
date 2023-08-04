from unittest import TestCase

from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.mongodb.MongoDataBase import MongoDataBase
from datetime import datetime


def toDate(date: str):
    return datetime.strptime(date, '%Y-%m-%d %H:%M')


class TestMongoDataBase(TestCase):
    mongoDb = MongoDataBase("config_database_test")

    def setUp(self):
        self.mongoDb.collection.drop()
        weathers = [WeatherData("Beijing", "", "CNs", "Partly cloudy", 36.5, 80, '2023-07-24 00:15'),
                    WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-24 00:25'),
                    WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-25 00:30'),
                    WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-26 01:13'),
                    WeatherData("Beijing", "", "CNs", "Partly cloudy", 36.5, 80, '2023-07-24 01:15'),
                    WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-25 02:30'),
                    WeatherData("Tapachula", "United Mexican States/Mexico", "MX", "Partly cloudy", 36.5, 80, '2023-07-27 02:30')]

        self.mongoDb.insert_weather(weathers)

    @classmethod
    def tearDownClass(cls):
        cls.mongoDb.clean()

    def test_get_weather_by_date(self):
        d24 = self.mongoDb.get_weather_by_date(toDate('2023-07-24 00:45'))
        self.assertIsInstance(d24[0], WeatherData)
        self.assertEqual(len(d24), 2)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-25 00:00'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-28 23:00'))), 0)

    def test_delete_old_weather(self):
        self.mongoDb.delete_old_weather(toDate("2023-07-25 00:00"))
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-24 00:00'))), 0)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-25 00:00'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-25 02:00'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-26 01:00'))), 1)
        self.assertEqual(len(self.mongoDb.get_weather_by_date(toDate('2023-07-28 00:00'))), 0)

    def test_get_similar_name(self):
        stored_name = self.mongoDb.get_by_similar_name("tapa").city_name
        self.assertIsNotNone(stored_name)
        self.assertEqual(stored_name, "Tapachula")
        stored_name = self.mongoDb.get_by_similar_name("Tapa").city_name
        self.assertEqual(stored_name, "Tapachula")

