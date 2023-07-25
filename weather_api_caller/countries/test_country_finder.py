from unittest import TestCase

from weather_api_caller.countries.country_finder import find_country, CountryName


class Test(TestCase):
    def test_find_country(self):
        country = CountryName(short_name="IS", country="Republic of Iceland/Iceland", city_name="Reykjavik")
        self.assertEqual(find_country("is"), country)
        self.assertEqual(find_country("IS"), country)
        self.assertEqual(find_country("Republic of Iceland"), country)
        self.assertEqual(find_country("Iceland"), country)
        self.assertEqual(find_country("Reykjavik"), country)
        self.assertEqual(find_country("reykjavik"), country)

        self.assertIsNone(find_country("dx"))
