import numpy as np

from data.WeatherData import WeatherData
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

    weathers_x = weathers_df[["humidity", "temperature"]].values
    weather_y = ref_df[["humidity", "temperature"]].values
    sim = np.array(cosine_similarity(weathers_x, weather_y)).reshape(-1)
    weathers_df["similarity"] = sim
    similar = weathers_df.sort_values(by="similarity", ascending=False).head(number_of_elements)
    return similar
