import requests
import logging

class CurrencyConverter:
    """
    A class to interact with a currency exchange API and fetch exchange rates.

    Attributes:
    - api_key (str): The API key for accessing the currency exchange API.
    """


    def __init__(self, converter_settings):
        """
        Initializes the CurrencyConverter with the provided API key.

        Args:
        - api_key (str): The API key for accessing the currency exchange API.
        """
        self._base_url = converter_settings["url"]
        self._host = converter_settings["api_host"]
        self._api_key = converter_settings["api_key"]
        self._headers = {
            "X-RapidAPI-Key": self._api_key,
            "X-RapidAPI-Host": self._host,
        }
        self._from_currencies = converter_settings["from_currencies_list"]
        self._to_currency = converter_settings["to_currency"]
        self._amount = converter_settings["amount"]


    def _make_request(self, params):
        """
        Makes a request to the currency exchange API.

        Args:
        - params (dict): Parameters to be sent with the request.

        Returns:
        - tuple: A tuple containing the status code and the JSON response data.
        """
        requests.packages.urllib3.disable_warnings()
        response = requests.get(self._base_url, headers=self._headers, params=params, verify=False)
        return (
            response.status_code,
            response.json() if response.status_code == 200 else None,
        )

    def _get_exchange_rate(self, from_currency, to_currency, amount=1.0):
        """
        Retrieves the exchange rate between two currencies.

        Args:
        - from_currency (str): The currency to convert from.
        - to_currency (str): The currency to convert to.
        - amount (float): The amount to convert (default is 1.0).

        Returns:
        - float: The exchange rate from the source currency to the target currency.
        """
        params = {"from": from_currency, "to": to_currency, "q": amount}
        status_code, data = self._make_request(params)

        if data:
            return data
        else:
            logging.warning(f"Failed to retrieve exchange rate. Error: {status_code}")
            return None

    def _fetch_and_log_exchange_rate(self, from_currency, to_currency, amount=1.0):
        """
        Fetches and logs the exchange rate between two currencies.

        Args:
        - from_currency (str): The currency to convert from.
        - to_currency (str): The currency to convert to.
        - amount (float): The amount to convert (default is 1.0).

        Returns:
        - float: The exchange rate from the source currency to the target currency.
        """
        exchange_rate = self._get_exchange_rate(from_currency, to_currency, amount)

        if exchange_rate:
            logging.debug(
                f"Exchange rate from {from_currency} to {to_currency} for {amount} is: {exchange_rate}"
            )
        else:
            logging.warning("Failed to retrieve exchange rate.")

        return exchange_rate


    def get_exchange_rates(self):
        """
        Publish exchange rates to Kafka topic.

        Args:
        - converter (CurrencyConverter): The currency converter object.
        - producer (Producer): The Kafka producer object.
        - currencies (list): List of currencies to convert.
        - to_currency (str): The target currency for conversion.
        - amount (float): The amount to convert.
        - query_interval (int): Time interval between queries.
        """
        result = []
        for from_currency in self._from_currencies:
            exchange_rate = self._fetch_and_log_exchange_rate(
                from_currency, self._to_currency, self._amount
            )
            if exchange_rate:
                message = {
                    "from_currency": from_currency,
                    "to_currency": self._to_currency,
                    "rate": exchange_rate,
                }
                result.append({'rate': message})

        return result