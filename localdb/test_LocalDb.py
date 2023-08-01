import os
from unittest import TestCase

from localdb.LocalDb import LocalDB
from weather_api_caller.WeatherCaller import get_today


class TestLocalDB(TestCase):

    @classmethod
    def tearDownClass(cls):
        os.remove("tiny_weather_db.sqlite")

    def test_insert_and_clear(self):
        localdb = LocalDB()
        test_date = get_today()
        localdb.insert_query_history("MX", test_date)
        self.assertEqual(localdb.get_query_history("MX"), test_date)
        self.assertIsNone(localdb.get_query_history("JP"))
        self.assertEqual(1, localdb.get_history_count())
        localdb.insert_query_history("JP", test_date)
        self.assertEqual(2, localdb.get_history_count())
        localdb.conn.close()
