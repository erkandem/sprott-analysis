"""
Define, scrape and store information locally from the Sprott AM web app.
"""
import json
import re
from datetime import date
from pathlib import Path
from typing import Optional, TypeVar, Union

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup

LOCAL_PATH = Path(".").resolve()
STORAGE_FOLDER = "data"
STORAGE_PATH = LOCAL_PATH / STORAGE_FOLDER


def extract_series_string(script_tag: bs4.Tag) -> str:
    """
    the "series" key is found one time in the chart element, and it is an array of objects.
    """
    start = script_tag.text.find("series:")
    found = 0
    end = -1
    for m in re.finditer(r"[\[\]]", script_tag.text):
        if m.start() < start:
            continue
        if m.group() == "[":
            found += 1
        elif m.group() == "]":
            found -= 1
        if found == 0:
            end = m.end()
            break
    series = script_tag.text[start:end] if end > -1 else None
    if series is None:
        raise ValueError("Nothing found")
    return series


def extract_data(series_string: str) -> dict[str, Optional[str]]:
    """extract all present series names and data within a series array

    Args:
        series_string: string, which contains the arrays of data to be extracted
    """
    series_names = re.findall("name:[\s]*'(.*)'", series_string)
    series_data_ = {}
    for idx, data_match in enumerate(re.finditer(r"data:", series_string)):
        start = data_match.end()
        found = 0
        end = -1
        for m in re.finditer(r"[\[\]]", series_string):
            if m.start() < start:
                continue
            if m.group() == "[":
                found += 1
            elif m.group() == "]":
                found -= 1
            if found == 0:
                end = m.end()
                break
        data = series_string[start:end].strip() if end else None
        series_data_[series_names[idx]] = data
    return series_data_


def _deserialize_date(data: list[list[str, int]]) -> list[list[date, int]]:
    """deserialize all dates in the string to python ``datetime.date`` objects"""
    date_re_key_with_groups = re.compile(
        r"Date.UTC\((?P<year>[0-9]{4}),(?P<month>[0-9]{1,2}),(?P<day>[0-9]{1,2})\)"
    )
    for idx, elm in enumerate(data):
        m = re.match(date_re_key_with_groups, data[idx][0])
        data[idx][0] = date(
            int(m.group("year")),
            int(m.group("month"))
            + 1,  # for some reason the month values in the feed range from 0 to 11
            int(m.group("day")),
        )
    return data


def deserialize_series_data(series_data: dict[str, str]) -> dict[str, list[date, int]]:
    """deserialize the JS string to python object(s)"""
    for series_name, series in series_data.items():
        series_escaped_date = re.sub(
            r"Date.UTC\([0-9]{4},[0-9]{1,2},[0-9]{1,2}\)",
            lambda x: '"%s"'
            % x.group(),  # making the string deserializable for the json module
            series,
        )
        partially_deserialized: list[list[str, int]] = json.loads(series_escaped_date)
        fully_deserialized: list[list[date, int]] = _deserialize_date(
            partially_deserialized
        )
        series_data[series_name] = fully_deserialized
    return series_data


class SprottWebPageScrapeConfig:
    def __repr__(self):
        return self.product

    product: str
    url: str
    price_vs_nav_placeholder: str
    premium_discount_placeholder: str
    premium_discount_to_nav_title: str = "Premium/Discount to Net Asset Value"
    nav_title: str = "Net Asset Value"
    share_price_title: str = "Share Price"

    @classmethod
    def get_slug(cls):
        return cls.product.replace(" ", "-").lower()


SprottWebPageScrapeConfigType = TypeVar(
    "SprottWebPageScrapeConfigType", bound=SprottWebPageScrapeConfig
)


class SprottSilver(SprottWebPageScrapeConfig):
    product = "silver"
    url = "https://sprott.com/investment-strategies/physical-bullion-trusts/gold-and-silver/"
    price_vs_nav_placeholder = "silver_Market_Price_Vs_NAV_Graph_Placeholder"
    premium_discount_placeholder = "silver_PDC_Graph_Placeholder"


class SprottGoldAndSilver(SprottWebPageScrapeConfig):
    product = "gold and silver"
    url = "https://sprott.com/investment-strategies/physical-bullion-trusts/gold-and-silver/"
    price_vs_nav_placeholder = "gold_silver_Market_Price_Vs_NAV_Graph_Placeholder"
    premium_discount_placeholder = "gold_silver_PDC_Graph_Placeholder"


class SprottUranium(SprottWebPageScrapeConfig):
    product = "uranium"
    url = "https://sprott.com/investment-strategies/physical-commodity-funds/uranium/"
    price_vs_nav_placeholder = "uranium_Market_Price_Vs_NAV_Graph_Placeholder"
    premium_discount_placeholder = "uranium_PDC_Graph_Placeholder"


class SprottGold(SprottWebPageScrapeConfig):
    product = "gold"
    url = "https://sprott.com/investment-strategies/physical-bullion-trusts/gold/"
    price_vs_nav_placeholder = "gold_Market_Price_Vs_NAV_Graph_Placeholder"
    premium_discount_placeholder = "gold_PDC_Graph_Placeholder"


class SprottESGGold(SprottWebPageScrapeConfig):
    product = "ESG gold"
    url = "https://sprott.com/investment-strategies/sesg-gold-etf/"
    price_vs_nav_placeholder = "esg_gold_Market_Price_Vs_NAV_Graph_Placeholder"
    premium_discount_placeholder = "esg_gold_PDC_Graph_Placeholder"


class SprottPlatinumAndPalladium(SprottWebPageScrapeConfig):
    product = "platinum and palladium"
    url = "https://sprott.com/investment-strategies/physical-bullion-trusts/platinum-and-palladium/"
    price_vs_nav_placeholder = (
        "platinum_palladium_Market_Price_Vs_NAV_Graph_Placeholder"
    )
    premium_discount_placeholder = "platinum_palladium_PDC_Graph_Placeholder"


product_configurations = {
    0: SprottUranium,
    1: SprottSilver,
    2: SprottGold,
    3: SprottESGGold,
    4: SprottPlatinumAndPalladium,
    5: SprottGoldAndSilver,
}


def get_premium_discount_data(config: SprottWebPageScrapeConfigType) -> pd.DataFrame:
    """requests, parses and returns a data on the Sprott product pages and
    returns a DataFrame object containing

    Args:
        config: a child of ``SprottWebPageScrapeConfig``

    Returns:
        pd.DataFrame:

    """
    response = requests.get(config.url)
    soup = BeautifulSoup(response.text, "lxml")
    result = {}
    placeholder_to_scrape = (
        config.premium_discount_placeholder,
        config.price_vs_nav_placeholder,
    )

    for placeholder_string in placeholder_to_scrape:
        script_tags = soup.find_all(
            "script"
        )  # No, the string=substring arg does not work in this case
        target_script_tag = None
        for ind, elm in enumerate(script_tags):
            if placeholder_string in elm.text:
                target_script_tag = elm
                break
        series_string_ = extract_series_string(target_script_tag)
        series_data = extract_data(series_string_)
        series_data = deserialize_series_data(series_data)
        result[placeholder_string] = series_data

    pd_df = pd.DataFrame.from_records(
        result[config.premium_discount_placeholder][
            config.premium_discount_to_nav_title
        ],
        columns=("date", "premium_pct"),
    )
    nav_df = pd.DataFrame.from_records(
        result[config.price_vs_nav_placeholder][config.nav_title],
        columns=("date", "nav"),
    )
    price_df = pd.DataFrame.from_records(
        result[config.price_vs_nav_placeholder][config.share_price_title],
        columns=("date", "price"),
    )
    pd_df.drop_duplicates("date", inplace=True)
    nav_df.drop_duplicates("date", inplace=True)
    price_df.drop_duplicates("date", inplace=True)
    pd_df.set_index("date", drop=True, inplace=True)
    nav_df.set_index("date", drop=True, inplace=True)
    price_df.set_index("date", drop=True, inplace=True)
    joined_df = pd_df.join(price_df).join(nav_df)
    return joined_df


def write_results_to_json(
    result_df: pd.DataFrame,
    config: SprottWebPageScrapeConfigType,
):
    """writes the data of the DataFrame to a file in JSON format in the target location"""
    file_name = f"{config.get_slug()}.json"
    file_path = STORAGE_PATH / file_name
    with open(file_path, "w+") as file:
        result_df.reset_index().to_json(
            file, orient="records", date_format="epoch", indent=2
        )


def get_descriptive_statistics(
    results: pd.DataFrame,
    column: str,
) -> dict[str, Union[int, str]]:
    """calculates and returns some descriptive statistics of the DataFrane as a dictionary"""
    if column not in results.keys():
        raise KeyError
    return {
        "sample_size": len(results),
        "min [pct]": results[column].min(),
        "max [pct]": results[column].max(),
        "mean [pct]": results[column].mean(),
        "median [pct]": results[column].median(),
        ("latest [%s]" % results.iloc[-1].name): results.iloc[-1][column],
    }


if __name__ == "__main__":
    for config_class in product_configurations.values():
        result_df = get_premium_discount_data(config_class)
        write_results_to_json(result_df, config_class)
        desc_stats = get_descriptive_statistics(result_df, "premium_pct")
        print(
            "Statistics on the Premium as a Percentage of the NAV on %s"
            % config_class.get_slug()
        )
        for key, value in desc_stats.items():
            print(key, value)
