import json
import logging
import subprocess
import time
from threading import Thread
from kafka_publisher.api.currency_converter import CurrencyConverter
from kafka_publisher.producer import Producer
from kafka_publisher.consumer import Consumer

def configure_logging():
    """
    Configure logging for the application.
    """
    logging.basicConfig(level=logging.INFO)

def read_settings(file_path):
    """
    Read settings from a JSON file.

    Args:
    - file_path (str): Path to the JSON settings file.

    Returns:
    - dict: Dictionary containing the settings.
    """
    with open(file_path, "r") as f:
        settings = json.load(f)
    return settings

def consume_exchange_rates(consumer):
    """
    Consume exchange rates from Kafka topic.

    Args:
    - consumer (Consumer): The Kafka consumer object.
    """
    try:
        for received_msg in consumer.read():
            print(f"Received message: {received_msg}")
    except KeyboardInterrupt:
        logging.info("Consumer thread terminated by user.")

def start_spark_stream(spark_settings):
    """
    Start the Spark application using spark-submit.

    Args:
    - settings (dict): Dictionary containing application settings.
    """
    try:
        spark_submit_command = [
            "spark-submit",
            "--packages",
            f"{spark_settings['package_name']}:{spark_settings['package_version']}",
            spark_settings['spark_script_path']
        ]
        
        # Redirect output and error streams to /dev/null
        with open("/dev/null", "w") as null_output:
            subprocess.run(spark_submit_command, check=True, stdout=null_output, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: spark-submit command failed with return code {e.returncode}")
        
def start_app(settings):
    """
    Start the Kafka application.

    Args:
    - settings (dict): Dictionary containing application settings.
    """


    # create and start threads
    # spark_thread = Thread(target=start_spark_stream, args=(settings["spark"],))    
    # spark_thread.start()
    # time.sleep(5) # allow the spark stream to start before kafka producer

    # create currency converter object
    converter_settings = settings["currency_converter"]
    converter = CurrencyConverter(converter_settings)

    # start kafka thread
    kafka_settings = settings["kafka"]
    publish_interval = kafka_settings["publish_interval"]  # seconds
    
    producer = Producer(kafka_settings, converter)

    kafka_producer_thread = Thread(
        target=producer.publish_exchange_rates,
        args=(
           publish_interval,
        ),
    )
    kafka_producer_thread.start()
    
    # start consumer if needed
    if kafka_settings['start_consumer'] :
        consumer = Consumer(kafka_settings)
        kafka_consumer_thread = Thread(target=consume_exchange_rates, args=(consumer,))    
        kafka_consumer_thread.start()

    
if __name__ == "__main__":
    configure_logging()
    settings = read_settings("./app/settings.json")
    start_app(settings)
