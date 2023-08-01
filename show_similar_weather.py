import pandas as pd

from localdb.LocalDb import LocalDB
from weather_api_caller.WeatherCaller import WeatherCaller, get_today
from weather_api_caller.countries.country_finder import find_country, CountryName
from weather_api_caller.data.WeatherData import WeatherData
from weather_api_caller.similarity_calculator import calculate_similarity

from tabulate import tabulate

first_row_format = "Capital cities with weather conditions similar to {} today"
headers = ["Capital city, Country", "Weather Status", "Temperature", "Humidity"]


def get_weathers(country: CountryName, config: str = "config_test", date=get_today()) \
        -> tuple[list[WeatherData], WeatherData]:
    localdb = LocalDB("tiny_weather_db")
    stored = localdb.get_query_history(country.short_name)
    if stored:
        stored_date, weather_status = stored
        if stored_date == date:
            return localdb.get_weathers(country.short_name, weather_status)
    stored_date = localdb.get_history_date()
    if stored_date is None or stored_date != date:
        localdb.clear_weather()
        localdb.clear_history()
    api_caller = WeatherCaller(config)
    reference = api_caller.get_weather(country.short_name, date)

    if reference is None:
        api_caller.update_all_weathers()
        reference = api_caller.get_weather(country.short_name, date)

    similar = api_caller.get_similar_weather(country.short_name, date)
    localdb.insert_weather(similar)
    localdb.insert_query_history(country.short_name, date, reference.weather_status)
    localdb.conn.close()
    return similar, reference


def get_similar(place: str, config: str = "config_test", date=get_today(), quantity=5):
    place = find_country(place)
    if place is None:
        print("This place is not supported")
        exit()

    similar, reference = get_weathers(place, config, date)

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
