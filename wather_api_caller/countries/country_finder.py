from collections import namedtuple
import pkg_resources
import pandas as pd

file_path = pkg_resources.resource_filename(__name__, "countries.csv")
countries = pd.read_csv(file_path)
CountryName = namedtuple("CountryName", ["city_name", "short_name", "country"])


def find_country(country: str) -> CountryName | None:
    for column in countries.columns:
        matching = countries[countries[column].str.contains(country, case=False, na=False)]
        if len(matching) > 0:
            short_name, country_name, alt_country_name, city_name = matching.values.tolist()[0]
            if country_name != alt_country_name:
                country_name += f"/{alt_country_name}"
            return CountryName(city_name=city_name, short_name=short_name, country=country_name)
    return None
