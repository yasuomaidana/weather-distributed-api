from unittest import TestCase

from weather_api_caller.weather_api.WeatherApi import WeatherApi


class TestWeatherApi(TestCase):
    def test_get_country_weather(self):
        weather_api = WeatherApi("config_api_test")
        real_place = weather_api.get_country_weather("London")

        from_api = weather_api.call_api({"q": "London", "days": "3"})
        ri = real_place[0]
        fai = from_api[0]

        self.assertEqual(len(real_place), 3)
        self.assertIsNone(weather_api.get_country_weather("dx"))

        self.assertEqual(ri.temperature, fai.temperature)
        self.assertEqual(ri.weather_status, fai.weather_status)
        self.assertEqual(ri.humidity, fai.humidity)