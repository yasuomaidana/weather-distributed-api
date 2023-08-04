from unittest import TestCase

from weather_api_caller.time_utilery.time_builders import convert_to_local


class Test(TestCase):
    def test_convert_to_local(self):
        tz_id = "America/Mexico_City"
        epoch = 1691125200
        local_time = convert_to_local(epoch, tz_id)
        self.assertEqual(local_time.hour, 14)
