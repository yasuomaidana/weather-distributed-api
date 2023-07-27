from unittest import TestCase

from weather_api_caller.WeatherCaller import WeatherCaller
from weather_api_caller.similarity_calculator import calculate_similarity


class TestWeatherCaller(TestCase):
    def test_get_weather(self):
        weather_caller = WeatherCaller("config_test")
        weather_caller.update_all_weathers()
        weathers = weather_caller.get_weather("GB")

        self.assertIsNotNone(weathers)

    def test_get_similar(self):
        weather_caller = WeatherCaller("config_test")
        weather_caller.update_all_weathers()
        sim = weather_caller.get_similar_weather("mx")
        self.assertGreater(len(sim), 0)

    def test_get_similar_cos(self):
        weather_caller = WeatherCaller("config_test")
        weather_caller.update_all_weathers()
        y = weather_caller.get_weather("mx")
        x = weather_caller.get_similar_weather("mx")
        sim = calculate_similarity(x, y)
        self.assertIsNotNone(sim)
