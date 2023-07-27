from weather_api_caller.WeatherCaller import WeatherCaller, get_today
from weather_api_caller.countries.country_finder import find_country
from weather_api_caller.similarity_calculator import calculate_similarity

from tabulate import tabulate

first_row_format = "Capital cities with weather conditions similar to {} today"
headers = ["Capital city, Country", "Weather Status", "Temperature", "Humidity"]


def show_similar(place: str, config: str = "config_test", date=get_today(), quantity=5):
    place = find_country(place)
    if place is None:
        print("This place is not supported")
        return 

    api_caller = WeatherCaller(config)
    reference = api_caller.get_weather(place.short_name, date)
    similar = api_caller.get_similar_weather(place.short_name, date)

    similar = calculate_similarity(similar, reference, quantity)
    similar.drop(columns="date", inplace=True)
    similar["city_name"] = similar["city_name"] + ", " + similar["short_name"]
    similar.drop(columns=["short_name", "country_name"], inplace=True)
    similar = similar.values.tolist()

    ref = similar.pop(0)
    print(first_row_format.format(ref[0]))
    if len(similar) == 0:
        print(f"There is no capital with similar weather today")
        print("Weather today")
        similar = [ref]

    for row in similar:
        row[2] = f"{row[2]} degrees"
        row[3] = f"{row[3]}%"

    print(tabulate(similar, headers=headers, showindex="always", tablefmt="fancy_grid", numalign="right"))
