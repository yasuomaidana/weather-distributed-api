import pandas as pd

from weather_api_caller.WeatherCaller import WeatherCaller, get_today
from weather_api_caller.countries.country_finder import find_country
from weather_api_caller.similarity_calculator import calculate_similarity

from tabulate import tabulate

first_row_format = "Capital cities with weather conditions similar to {} today"
headers = ["Capital city, Country", "Weather Status", "Temperature", "Humidity"]


def get_similar(place: str, config: str = "config_test", date=get_today(), quantity=5):
    place = find_country(place)
    if place is None:
        print("This place is not supported")
        return

    api_caller = WeatherCaller(config)
    reference = api_caller.get_weather(place.short_name, date)

    if reference is None:
        api_caller.update_all_weathers()
        reference = api_caller.get_weather(place.short_name, date)

    similar = api_caller.get_similar_weather(place.short_name, date)

    similar = calculate_similarity(similar, reference, quantity)
    similar.drop(columns="date", inplace=True)

    ref_loc: pd.DataFrame = similar.loc[similar['short_name'] == reference.short_name].copy()

    similar.drop(ref_loc.index[0], inplace=True)
    similar["city_name"] = similar["city_name"] + ", " + similar["short_name"]
    ref_loc["city_name"] = ref_loc["city_name"] + ", " + ref_loc["short_name"]

    similar.drop(columns=["short_name", "country_name"], inplace=True)
    ref_loc.drop(columns=["short_name", "country_name"], inplace=True)
    similar = similar.values.tolist()

    ref = ref_loc.values.tolist()[0]
    return ref, similar


def show_similar(place: str, config: str = "config_test", date=get_today(), quantity=5):
    ref, similar = get_similar(place, config, date, quantity)
    print(first_row_format.format(ref[0]))
    if len(similar) == 0:
        print(f"There is no capital with similar weather today")
        print("Weather today")
        similar = [ref]

    for row in similar:
        row[2] = f"{row[2]} degrees"
        row[3] = f"{row[3]}%"

    print(tabulate(similar, headers=headers, showindex="always", tablefmt="fancy_grid", numalign="right"))
