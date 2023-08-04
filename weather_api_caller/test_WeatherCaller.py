from unittest import TestCase

from weather_api_caller.WeatherCaller import WeatherCaller
from weather_api_caller.similarity_calculator import calculate_similarity
from weather_api_caller.time_utilery.time_builders import get_future_hour


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

    def test_get_non_listed(self):
        weather_caller = WeatherCaller("config_test")
        weather_caller.update_all_weathers()
        y = weather_caller.get_weather("tapachula")
        x = weather_caller.get_similar_weather("tapachula")
        sim = calculate_similarity(x, y)
        self.assertIsNotNone(sim)
        self.assertEqual(sim.iloc[0]["city_name"], "Tapachula")


    def test_updating_another_hour(self):
        weather_caller = WeatherCaller("config_test")
        weather_caller.update_all_weathers(get_future_hour(5))

