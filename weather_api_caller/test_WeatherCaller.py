from unittest import TestCase

from weather_api_caller.WeatherCaller import WeatherCaller


class TestWeatherCaller(TestCase):
    def test_get_weather(self):
        weather_caller = WeatherCaller("config_test")
        weathers = weather_caller.get_weather()
        self.assertGreater(len(weathers), 0)
