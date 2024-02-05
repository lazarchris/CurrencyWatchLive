import json
import logging
from kafka import KafkaProducer


class Producer:
    def __init__(self, server, topic):
        self._server = server
        self._producer = KafkaProducer(bootstrap_servers=server)
        self._topic = topic

    def send_to_kafka_topic(self, message):
        try:
            logging.debug(f"Published message: {message}")
            serialized_msg = json.dumps(message).encode("utf-8")
            self._producer.send(self._topic, value=serialized_msg)
            self._producer.flush()
        except Exception as e:
            logging.error(f"Couldn't publish topic: {e}")
