import requests
import json
import pytest
import argparse


API_KEY = "sKLFJ3yeKEUnJpG4pZ9vh0OkDjUxtI7C"


def range_limited_float_type(arg):
    try:
        arg = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{arg} not a floating-point literal")

    if arg < 0:
        raise argparse.ArgumentTypeError(f"{arg} not greater than zero")
    return arg


def cli_arguments_reader() -> float:
    parser = argparse.ArgumentParser(description='Currency rate')
    parser.add_argument('threshold', type=range_limited_float_type, default=False,
                        help='The rate threshold')

    return parser.parse_args().threshold


def test_rate():
    assert get_currency_with_rate_lower_than_threshold({"USD": 1, "EUR": 0.9}, 1) == ["EUR"]
    assert get_currency_with_rate_lower_than_threshold({"USD": 1, "EUR": 0.9}, 0.9) == []


def test_get_data():
    assert len(get_data(1)) >= 1


def get_data(threshold: float = 10) -> list:
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {
        "apikey": API_KEY
    }
    response = requests.request("GET", url, headers=headers)
    result = response.text
    list_of_currencies = get_currency_with_rate_lower_than_threshold(json.loads(result)["rates"], threshold)
    return list_of_currencies


def get_currency_with_rate_lower_than_threshold(rates, threshold):
    list_of_currencies = []
    for currency, rate in rates.items():
        if rate < threshold:
            list_of_currencies.append(currency)

    return list_of_currencies


if __name__ == '__main__':
    arguments = cli_arguments_reader()
    get_data(threshold=arguments)
