from collections import namedtuple
from typing import List

import pkg_resources

import pandas as pd

file_path = pkg_resources.resource_filename(__name__, "countries.csv")
countries = pd.read_csv(file_path, na_values=[], keep_default_na=False)
CountryName = namedtuple("CountryName", ["city_name", "short_name", "country", "coordinate"])


def get_all_countries() -> List[str]:
    return list(zip(countries["country_code"].tolist(), countries["coordinate"].tolist()))


def find_country(country: str) -> CountryName | None:
    countries_names = countries.columns.tolist()
    [countries_names.remove(i) for i in ["coordinate"]]
    for column in countries_names:
        matching = countries[countries[column].str.contains(country, case=False, na=False)]
        if len(matching) > 0:
            short_name, country_name, alt_country_name, city_name, coordinate = matching.values.tolist()[0]
            if country_name != alt_country_name:
                country_name += f"/{alt_country_name}"
            return CountryName(city_name=city_name, short_name=short_name, country=country_name,
                               coordinate=coordinate)
    return None
