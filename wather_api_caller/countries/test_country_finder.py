from unittest import TestCase

from wather_api_caller.countries.country_finder import find_country


class Test(TestCase):
    def test_find_country(self):
        self.assertEqual(find_country("is"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
        self.assertEqual(find_country("IS"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
        self.assertEqual(find_country("Republic of Iceland"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
        self.assertEqual(find_country("Iceland"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
        self.assertEqual(find_country("Reykjavik"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
        self.assertEqual(find_country("reykjavik"), ['IS', 'Republic of Iceland', 'Iceland', 'Reykjavik'])
