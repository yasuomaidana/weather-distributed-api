from unittest import TestCase

from show_similar_weather import get_similar


class Test(TestCase):
    def test_get_similar(self):
        get_similar("jp")

