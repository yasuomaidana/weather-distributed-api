from unittest import TestCase

from weather_api_caller.countries.country_finder import find_country, CountryName, get_all_countries


class Test(TestCase):
    def test_find_country(self):
        country = CountryName(short_name="IS", country="Republic of Iceland/Iceland", city_name="Reykjavik",
                              coordinate="64.1462044,-21.9424373")

        self.assertEqual(find_country("is"), country)
        self.assertEqual(find_country("IS"), country)
        self.assertEqual(find_country("Republic of Iceland"), country)
        self.assertEqual(find_country("Iceland"), country)
        self.assertEqual(find_country("Reykjavik"), country)
        self.assertEqual(find_country("reykjavik"), country)

        self.assertIsNone(find_country("dx"))

    def test_get_all_countries(self):
        countries = get_all_countries()
        self.assertEqual(len(countries), 198)


