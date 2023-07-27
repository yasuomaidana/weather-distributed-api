import numpy as np

from weather_api_caller.data import WeatherData
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(weathers: list[WeatherData], reference: WeatherData, number_of_elements=5):
    weathers_df = pd.DataFrame({
        "city_name": [data.city_name for data in weathers],
        "country_name": [data.country_name for data in weathers],
        "short_name": [data.short_name for data in weathers],
        "weather_status": [data.weather_status for data in weathers],
        "temperature": [data.temperature for data in weathers],
        "humidity": [data.humidity for data in weathers],
        "date": [data.date for data in weathers]
    })

    ref_df = pd.DataFrame({
        "city_name": [reference.city_name],
        "country_name": [reference.country_name],
        "short_name": [reference.short_name],
        "weather_status": [reference.weather_status],
        "temperature": [reference.temperature],
        "humidity": [reference.humidity],
        "date": [reference.date]
    })

    def temperature_normalizer(x):
        return reference.temperature * np.exp(-(x - reference.temperature) ** 2)

    def humidity_normalizer(x):
        return np.exp(-(x - reference.humidity) ** 2)

    weathers_df["humidity_i"] = weathers_df["humidity"] \
        .apply(humidity_normalizer)
    ref_df["humidity_i"] = ref_df["humidity"] \
        .apply(humidity_normalizer)

    weathers_df["temperature_i"] = weathers_df["temperature"] \
        .apply(temperature_normalizer)
    ref_df["temperature_i"] = ref_df["temperature"] \
        .apply(temperature_normalizer)

    weathers_x = weathers_df[["humidity_i", "temperature_i"]].values
    weather_y = ref_df[["humidity_i", "temperature_i"]].values

    sim = np.array(cosine_similarity(weathers_x, weather_y)).reshape(-1)
    weathers_df["similarity"] = sim

    weathers_df = weathers_df[weathers_df["similarity"] > 0.9]

    weathers_df.drop(columns=["humidity_i", "temperature_i"], inplace=True)

    similar = weathers_df.sort_values(by="similarity", ascending=False).head(number_of_elements + 1)
    similar.drop(columns=["similarity"], inplace=True)
    return similar
