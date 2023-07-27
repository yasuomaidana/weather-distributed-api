from unittest import TestCase

from show_similar_weather import get_similar
from weather_api_caller.countries.country_finder import get_all_countries


class Test(TestCase):
    def test_get_similar(self):
        for short_name, i in get_all_countries():
            ref, _ = get_similar(short_name)
            self.assertEqual(short_name, ref[0].split(", ")[-1])
