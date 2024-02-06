import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, DoubleType

class KafkaToCSV:
    """
    Class to read data from Kafka topic, parse JSON messages, and write to CSV files using Apache Spark.
    """

    def __init__(self, kafka_bootstrap_servers, kafka_topic, output_path):
        """
        Initialize KafkaToCSV object.

        :param kafka_bootstrap_servers: Comma-separated list of Kafka bootstrap servers.
        :param kafka_topic: Kafka topic to subscribe to.
        :param output_path: Output path to write CSV files.
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
            .appName("KafkaToCSV") \
            .getOrCreate()

    def _read_from_kafka(self):
        """
        Read data from Kafka topic and parse JSON messages.

        :return: Parsed DataFrame.
        """
        schema = StructType() \
            .add("msg", StructType() \
                .add("from_currency", StringType()) \
                .add("to_currency", StringType()) \
                .add("rate", DoubleType()))

        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.kafka_topic) \
            .option("failOnDataLoss", "false") \
            .load()

        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", schema).alias("data")) \
            .select("data.msg.*")

        return parsed_df

    def _write_to_csv(self, parsed_df):
        """
        Write DataFrame to CSV file.

        :param parsed_df: DataFrame to write.
        """
        # Get current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Combine output path with current date
        output_file_path = os.path.join(self.output_path, current_date)

        # Write DataFrame to CSV file
        query = parsed_df \
            .writeStream \
            .outputMode("append") \
            .format("csv") \
            .option("path", output_file_path) \
            .option("checkpointLocation", "checkpoint_csv") \
            .start()

        query.awaitTermination()

    def process_kafka_to_csv(self):
        """
        Main method to process data from Kafka topic and write to CSV files.
        """
        parsed_df = self._read_from_kafka()
        self._write_to_csv(parsed_df)

if __name__ == "__main__":
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "topic_currency_exch_rate"
    output_path = "output_csv"

    kafka_to_csv = KafkaToCSV(kafka_bootstrap_servers, kafka_topic, output_path)
    kafka_to_csv.process_kafka_to_csv()
