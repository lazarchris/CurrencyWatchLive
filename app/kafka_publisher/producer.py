import json
import logging
import time
from kafka import KafkaProducer
from kafka_publisher.api.currency_converter import CurrencyConverter

class Producer:
    """
    A class for producing messages to a Kafka topic.

    Attributes:
    - server (str): The address of the Kafka server.
    - topic (str): The name of the Kafka topic to produce to.
    """

    def __init__(self, kafka_settings, currency_converter):
        """
        Initializes the Kafka producer.

        Args:
        - server (str): The address of the Kafka server.
        - topic (str): The name of the Kafka topic to produce to.
        """
        self._server =  f"{kafka_settings['host']}:{kafka_settings['port']}"
        self._topic = kafka_settings['topic']
        self._currency_converter = currency_converter
        self._producer = KafkaProducer(bootstrap_servers=self._server)
        

    def _send_to_kafka_topic(self, message):
        """
        Sends a message to the Kafka topic.

        Args:
        - message (dict): The message to be sent.

        Raises:
        - Exception: If an error occurs while sending the message.
        """
        try:
            logging.debug(f"Published message: {message}")
            serialized_msg = json.dumps(message).encode("utf-8")
            self._producer.send(self._topic, value=serialized_msg)
            self._producer.flush()
        except Exception as e:
            logging.error(f"Couldn't publish topic: {e}")

    def publish_exchange_rates(self, interval):
        """
        Publish exchange rates to Kafka topic.

        Args:
        - interval:  Publish msg between intervals
        """
        try:
            while True:
                for exchange_rate in self._currency_converter.get_exchange_rates():
                    self._send_to_kafka_topic({'msg': exchange_rate})
            
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Exchange rate publishing terminated by user.")
            
   
