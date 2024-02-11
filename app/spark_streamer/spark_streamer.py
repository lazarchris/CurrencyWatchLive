import os
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, concat_ws
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

class SparkStreamer:
    """
    Class to read data from Kafka topic, parse JSON messages, and append to a text file using Apache Spark.
    """

    def __init__(self, kafka_bootstrap_servers, kafka_topic, output_path):
        """
        Initialize SparkStreamer object.

        :param kafka_bootstrap_servers: Comma-separated list of Kafka bootstrap servers.
        :param kafka_topic: Kafka topic to subscribe to.
        :param output_path: Output path to write text files.
        """
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic
        self.output_path = output_path
        self.spark = self._create_spark_session()

    def _create_spark_session(self):
        """
        Create a SparkSession.

        :return: SparkSession object.
        """
        return SparkSession.builder \
            .appName("SparkStreamer") \
            .getOrCreate()

    def _read_from_kafka(self):
        """
        Read data from Kafka topic and parse JSON messages.

        :return: Parsed DataFrame.
        """
        schema = StructType([
            StructField("msg", StructType([
                StructField("rate", StructType([
                    StructField("from_currency", StringType()),
                    StructField("to_currency", StringType()),
                    StructField("rate", DoubleType())
                ]))
            ]))
        ])

        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.kafka_topic) \
            .option("failOnDataLoss", "false") \
            .load()

        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", schema).alias("data")) \
            .select("data.msg.rate.*")

        return parsed_df

    def _write_to_text_file(self, batch_df, batch_id):
        """
        Write DataFrame to a single text file.

        :param batch_df: DataFrame representing a batch of data.
        :param batch_id: ID of the batch.
        """
        # Concatenate column values into a single string with delimiter ','
        concatenated_df = batch_df.withColumn("data", concat_ws(",", col("from_currency"), col("to_currency"), col("rate")))

        # Select only the concatenated column
        selected_df = concatenated_df.select("data")

        # Write DataFrame to text file
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_file = os.path.join(self.output_path, f"output_{current_date}.txt")
        selected_df.coalesce(1).write.mode("append").text(output_file)

    def process_kafka_to_text_file(self):
        """
        Main method to process data from Kafka topic and write to a single text file.
        """
        parsed_df = self._read_from_kafka()

        # Process the DataFrame and write to a single text file
        parsed_df.writeStream.foreachBatch(self._write_to_text_file).start().awaitTermination()

if __name__ == "__main__":
    settings_file_path = "./app/settings.json"

    # Check if the settings file exists
    if not os.path.exists(settings_file_path):
        print("Error: settings file not found.")
        exit(1)

    try:
        # Load settings from JSON file
        with open(settings_file_path, "r") as f:
            settings = json.load(f)
    except Exception as e:
        print("Error:", e)
        exit(1)

    # Extract Kafka settings
    kafka_settings = settings.get("kafka", {})
    kafka_bootstrap_servers = f"{kafka_settings.get('host')}:{kafka_settings.get('port')}"
    kafka_topic = kafka_settings.get("topic")

    # Initialize SparkStreamer object
    kafka_to_text_file = SparkStreamer(kafka_bootstrap_servers, kafka_topic, "output_text")  # Assuming output_path is fixed as "output_text"
    
    # Process Kafka messages
    kafka_to_text_file.process_kafka_to_text_file()