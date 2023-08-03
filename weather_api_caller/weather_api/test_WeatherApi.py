from unittest import TestCase

from weather_api_caller.weather_api.WeatherApi import WeatherApi


class TestWeatherApi(TestCase):
    def test_get_country_weather(self):
        weather_api = WeatherApi("config_api_test")

        from_api = weather_api.call_api({"q": "London", "days": "1"})

        self.assertEqual(len(from_api), 24)
        self.assertIsNone(weather_api.call_api({"q": "3x", "days": "1"}))