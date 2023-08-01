import os
from unittest import TestCase

from localdb.LocalDb import LocalDB
from weather_api_caller.WeatherCaller import get_today
from weather_api_caller.data.WeatherData import WeatherData


class TestLocalDB(TestCase):
    localdb = LocalDB("tiny_sql_test")

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.localdb.conn.close()
        os.remove("tiny_sql_test.sqlite")

    def tearDown(self):
        self.localdb.clear_weather()
        self.localdb.clear_history()

    def test_insert_and_clear_query_history(self):
        localdb = self.localdb
        test_date = get_today()
        localdb.insert_query_history("MX", test_date)
        self.assertEqual(localdb.get_query_history("MX"), test_date)
        self.assertIsNone(localdb.get_query_history("JP"))
        self.assertEqual(1, localdb.get_history_count())
        localdb.insert_query_history("JP", test_date)
        self.assertEqual(2, localdb.get_history_count())
        localdb.clear_history()
        self.assertEqual(0, localdb.get_history_count())

    def test_insert_weather(self):
        localdb = self.localdb
        weather = WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-24')
        localdb.insert_weather(weather)
        self.assertEqual(1, localdb.get_weather_count())
        localdb.insert_weather(weather)
        self.assertEqual(1, localdb.get_weather_count())
        weather = WeatherData("Mexico City", "", "MX", "Partly cloudy", 36.5, 80, '2023-07-25')
        localdb.insert_weather(weather)
        self.assertEqual(2, localdb.get_weather_count())
        localdb.clear_weather()
        self.assertEqual(0, localdb.get_weather_count())

    def test_insert_weathers(self):
        localdb = self.localdb
        weathers = [WeatherData("Beijing", "", "CN", "Partly cloudy", 36.5, 80, '2023-07-24'),
                    WeatherData("Mexico City", "", "MX", "Partly cloudy", 36.5, 80, '2023-07-25')]
        self.localdb.insert_weather(weathers)
        self.assertEqual(2, localdb.get_weather_count())
        self.localdb.insert_weather(weathers)
        self.assertEqual(2, localdb.get_weather_count())
        localdb.clear_weather()
        self.assertEqual(0, localdb.get_weather_count())
