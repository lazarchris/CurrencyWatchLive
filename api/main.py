import requests
import logging
import time
from CurrencyConverter import CurrencyConverter


def configure_logging():
    logging.basicConfig(level=logging.INFO)


def start_app():
    api_key = "64f575c77dmshbeab56d45cba627p1a86bdjsn0cc5c5a4d56c"
    converter = CurrencyConverter(api_key)

    currencies_to_convert = ["EUR", "JPY", "GBP", "AUD", "CAD"]
    to_currency = "USD"
    amount = 1.0

    try:
        while True:
            for from_currency in currencies_to_convert:
                converter.fetch_and_log_exchange_rate(
                    from_currency, to_currency, amount
                )
            # Sleep for 1 hour (3600 seconds)
            time.sleep(3600)
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")


if __name__ == "__main__":
    configure_logging()
    start_app()
