"""
Currency Converter (CLI)

A command-line currency converter that uses CurrencyConverterAPI endpoints.

Requirements:
(i) Environment variable: CURRENCY_API_KEY;
(ii) Dependency: requests.

Notes:
- The free API may be unavailable at times (service-side limitation).
"""

import os
from typing import Any
import requests

BASE_URL = "https://free.currconv.com/"
API_KEY = os.getenv("CURRENCY_API_KEY")

def api_get_json(endpoint: str, timeout: int = 10) -> dict[str, Any]:
    """
    Perform a GET request to the CurrencyConverterAPI and return JSON.

    Args:
        endpoint: API endpoint path (without BASE_URL).
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as dict.

    Raises:
        RuntimeError: If API key is missing.
        requests.RequestException: For network / HTTP errors.
        ValueError: If JSON parsing fails.
    """
    if not API_KEY:
        raise RuntimeError("CURRENCY_API_KEY is not set. Export it or put it in your .env.")

    url = BASE_URL + endpoint
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def get_currencies() -> list[tuple[str, dict[str, Any]]]:
    """
    Fetch the list of supported currencies.

    Returns:
        Sorted list of (currency_code, currency_info_dict).
    """
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    data = api_get_json(endpoint).get("results", {})
    items = list(data.items())
    items.sort(key=lambda x: x[0])
    return items

def print_currencies(currencies: list[tuple[str, dict[str, Any]]]) -> None:
    """
    Print currencies in a readable format.

    Args:
        currencies: Output of get_currencies().
    """
    for _, currency in currencies:
        name = currency.get("currencyName", "")
        code = currency.get("id", "")
        symbol = currency.get("currencySymbol", "")
        print(f"{code} - {name} - {symbol}")

def exchange_rate(cur1: str, cur2: str) -> float | None:
    """
    Fetch exchange rate from cur1 to cur2.

    Args:
        cur1: Base currency code (e.g., USD).
        cur2: Target currency code (e.g., EUR).

    Returns:
        Rate as float, or None if conversion is invalid / not found.
    """
    pair = f"{cur1}_{cur2}"
    endpoint = f"api/v7/convert?q={pair}&compact=ultra&apiKey={API_KEY}"
    data = api_get_json(endpoint)

    if not data:
        print("Invalid currencies or empty response.")
        return None

    rate = data.get(pair)
    if rate is None:
        print("Invalid currencies or unsupported pair.")
        return None

    print(f"{cur1} -> {cur2} = {rate}")
    return float(rate)

def convert(cur1: str, cur2: str, amount: str) -> float | None:
    """
    Convert an amount from one currency to another.

    Args:
        cur1: Base currency code.
        cur2: Target currency code.
        amount: Amount as string (user input).

    Returns:
        Converted amount, or None if invalid.
    """
    rate = exchange_rate(cur1, cur2)
    if rate is None:
        return None

    try:
        value = float(amount)
    except ValueError:
        print("Invalid amount.")
        return None

    converted = rate * value
    print(f"{value} {cur1} is equal to {converted:.4f} {cur2}")
    return converted

def main() -> None:
    """
    CLI entry point.
    """
    print(
        "Hello! Commands:\n"
        "- list: show available currencies\n"
        "- rate: show exchange rate between two currencies\n"
        "- convert: convert an amount\n"
        "- q: quit\n"
    )

    currencies_cache: list[tuple[str, dict[str, Any]]] | None = None

    while True:
        command = input("Enter a command (q to quit): ").strip().lower()

        if command == "q":
            break

        try:
            if command == "list":
                if currencies_cache is None:
                    currencies_cache = get_currencies()
                print_currencies(currencies_cache)

            elif command == "convert":
                cur1 = input("Enter a currency you have: ").strip().upper()
                amount = input(f"Enter an amount in {cur1}: ").strip()
                cur2 = input("Enter a currency you want to get: ").strip().upper()
                convert(cur1, cur2, amount)

            elif command == "rate":
                cur1 = input("Enter a currency you have: ").strip().upper()
                cur2 = input("Enter a currency to convert to: ").strip().upper()
                exchange_rate(cur1, cur2)

            else:
                print("Unrecognized command.")

        except requests.RequestException as e:
            print(f"Network/API error: {e}")
        except RuntimeError as e:
            print(e)
            break
        except ValueError:
            print("Failed to parse API response.")

if __name__ == "__main__":
    main()
