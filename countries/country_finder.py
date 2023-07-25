import pandas as pd

countries = pd.read_csv("countries.csv")


def find_country(country: str):
    for column in countries.columns:
        matching = countries[countries[column].str.contains(country, case=False, na=False)]
        if len(matching) > 0:
            return matching.values.tolist()[0]
    return None
