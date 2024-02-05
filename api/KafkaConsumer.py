import json
import logging
from kafka import KafkaConsumer


class Consumer:
    def __init__(
        self,
        topic,
        server,
    ):
        """ """
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=server,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

    def read(self):
        """ """
        try:
            for msg in self._consumer:
                logging.debug(f"Received message: {msg}")
                yield msg
        except Exception as e:
            logging.error(f"Couldn't read topic: {e}")
