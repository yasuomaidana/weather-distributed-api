import datetime

from weather_api_caller.WeatherCaller import WeatherCaller, get_today
from weather_api_caller.countries.country_finder import find_country
from weather_api_caller.similarity_calculator import calculate_similarity

first_row_format = "Capital cities with weather conditions similar to {}, {} today"
row_format = "{}. {}, {}, {}, {} degrees, {}%"


def show_similar(place: str, config: str = "config_test", date=get_today(), quantity=5):

    place = find_country(place)
    if place is None:
        print("This place is not supported")

    api_caller = WeatherCaller(config)
    reference = api_caller.get_weather(place.short_name, date)
    similar = api_caller.get_similar_weather(place.short_name, date)

    similar: list = calculate_similarity(similar, reference, quantity).values.tolist()
    ref = similar.pop(0)
    print(first_row_format.format(ref[0], ref[2]))
    for i, weather in enumerate(similar):
        print(row_format.format(i+1, weather[0], weather[2], weather[3], weather[4], weather[5]))


if __name__ == "__main__":
    print("*****" * 15)

    show_similar("JP")
    print("*****" * 15)
    show_similar("MX")
    print("*****" * 15)
    show_similar("CA")
