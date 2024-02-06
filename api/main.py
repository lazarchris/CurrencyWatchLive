import logging
import time
from threading import Thread
from CurrencyConverter import CurrencyConverter
from KafkaConsumer import Consumer
from KafkaProducer import Producer


def configure_logging():
    logging.basicConfig(level=logging.INFO)


def consume_exchange_rates(consumer):
    try:
        for received_msg in consumer.read():
            print(f"Received message: {received_msg}")
    except KeyboardInterrupt:
        logging.info("Consumer thread terminated by user.")


def publish_exchange_rates(converter, producer, currencies, to_currency, amount, query_interval):
    try:
        while True:
            for from_currency in currencies:
                exchange_rate = converter.fetch_and_log_exchange_rate(
                    from_currency, to_currency, amount
                )
                if exchange_rate:
                    message = {
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "rate": exchange_rate,
                    }
                    producer.send_to_kafka_topic({'msg': message})
            time.sleep(query_interval)
    except KeyboardInterrupt:
        logging.info("Exchange rate publishing terminated by user.")


def start_app(server, topic):
    api_key = "64f575c77dmshbeab56d45cba627p1a86bdjsn0cc5c5a4d56c"
    converter = CurrencyConverter(api_key)
    producer = Producer(server, topic)
    consumer = Consumer(topic, server)

    currencies_to_convert = ["EUR", "JPY", "GBP", "AUD", "CAD"]
    to_currency = "USD"
    amount = 1.0
    query_interval = 10  # seconds

    # Create and start threads
    consumer_thread = Thread(target=consume_exchange_rates, args=(consumer,))
    producer_thread = Thread(
        target=publish_exchange_rates,
        args=(
            converter,
            producer,
            currencies_to_convert,
            to_currency,
            amount,
            query_interval,
        ),
    )

    producer_thread.start()
    consumer_thread.start()


if __name__ == "__main__":
    configure_logging()
    topic = "topic_currency_exch_rate"
    start_app("localhost:9092", topic)
