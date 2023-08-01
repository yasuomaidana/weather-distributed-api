import os
from unittest import TestCase

from localdb.LocalDb import LocalDB
from weather_api_caller.WeatherCaller import get_today


class TestLocalDB(TestCase):
    localdb = LocalDB("tiny_sql_test")

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.localdb.conn.close()
        os.remove("tiny_sql_test.sqlite")

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
