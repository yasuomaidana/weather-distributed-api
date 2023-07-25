from unittest import TestCase

from weather_api_caller.weather_api.WeatherApi import WeatherApi


class TestWeatherApi(TestCase):
    def test_get_country_weather(self):
        weather_api = WeatherApi("config_api_test")
        real_place = weather_api.get_country_weather("London")
        self.assertEqual(len(real_place), 3)
        self.assertEqual(weather_api.get_country_weather("dx"), [])
