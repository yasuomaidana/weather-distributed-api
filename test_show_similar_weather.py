import time
from unittest import TestCase

from localdb.LocalDb import LocalDB
from show_similar_weather import get_similar
from weather_api_caller.WeatherCaller import get_tomorrow
from weather_api_caller.countries.country_finder import get_all_countries


class Test(TestCase):
    def test_get_similar(self):
        for short_name, i in get_all_countries():
            ref, _ = get_similar(short_name)
            self.assertEqual(short_name, ref[0].split(", ")[-1])

    def test_compare_with_without_local_db(self):
        localdb = LocalDB("tiny_weather_db")
        localdb.clear_history()
        localdb.clear_weather()

        start_time = time.time()
        self.test_get_similar()
        end_time = time.time()
        without_ldb = end_time - start_time

        start_time = time.time()
        self.test_get_similar()
        end_time = time.time()
        with_ldb = end_time - start_time

        self.assertGreater(without_ldb, with_ldb)

    def test_get_another_day(self):
        localdb = LocalDB("tiny_weather_db")
        self.test_get_similar()
        self.assertEqual(localdb.get_weather_count(), 198)
        get_similar("mx", date=get_tomorrow())
        self.assertLess(localdb.get_weather_count(), 198)
