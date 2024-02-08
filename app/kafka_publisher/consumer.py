import json
import logging
from kafka import KafkaConsumer


class Consumer:
    """
    A class for consuming messages from a Kafka topic.

    Attributes:
    - topic (str): The name of the Kafka topic to consume from.
    - server (str): The address of the Kafka server.
    """

    def __init__(
        self,
        kafka_settings
    ):
        """
        Initializes the Kafka consumer.

        Args:
        - topic (str): The name of the Kafka topic to consume from.
        - server (str): The address of the Kafka server.
        """
        self._server = f"{kafka_settings['host']}:{kafka_settings['port']}"
        self._topic = kafka_settings['topic']
        
        self._consumer = KafkaConsumer(
            self._topic,
            bootstrap_servers=self._server,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

    def read(self):
        """
        Reads messages from the Kafka topic.

        Yields:
        - dict: A message read from the Kafka topic.
        """
        try:
            for msg in self._consumer:
                logging.debug(f"Received message: {msg}")
                yield msg
        except Exception as e:
            logging.error(f"Couldn't read topic: {e}")
