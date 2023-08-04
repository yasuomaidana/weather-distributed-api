import time
from unittest import TestCase

from localdb.LocalDb import LocalDB
from show_similar_weather import get_similar
from weather_api_caller.countries.country_finder import get_all_countries, find_country
from weather_api_caller.time_utilery.time_builders import get_future_hour


class Test(TestCase):
    def test_get_similar(self):
        for short_name, i in get_all_countries():
            country = find_country(short_name)
            ref, _ = get_similar(country.city_name)
            self.assertEqual(short_name, country.short_name)
            # self.assertTrue(country.city_name in ref[0])

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

    def test_get_another_hour(self):
        localdb = LocalDB("tiny_weather_db")
        get_similar("mx", date=get_future_hour(9))
        self.assertLess(localdb.get_weather_count(), 198)
