from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaToCSV") \
        .getOrCreate()

def read_from_kafka(spark, kafka_bootstrap_servers, kafka_topic):
    # Define the schema for the JSON messages
    schema = StructType() \
        .add("msg", StructType() \
            .add("from_currency", StringType()) \
            .add("to_currency", StringType()) \
            .add("rate", DoubleType()))

    # Read from Kafka using Structured Streaming
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    # Parse JSON messages
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", schema).alias("data")) \
        .select("data.msg.*")

    return parsed_df

def write_to_csv(parsed_df, output_path):
    # Write the parsed DataFrame to a CSV file
    query = parsed_df \
        .writeStream \
        .outputMode("append") \
        .format("csv") \
        .option("path", output_path) \
        .option("checkpointLocation", "checkpoint_csv") \
        .start()

    # Await termination
    query.awaitTermination()

if __name__ == "__main__":
    # Define Kafka source options
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "topic_currency_exch_rate"
    
    # Define output path for CSV file
    output_path = "output_csv"

    # Create Spark session
    spark = create_spark_session()

    # Read from Kafka
    parsed_df = read_from_kafka(spark, kafka_bootstrap_servers, kafka_topic)

    # Write to CSV
    write_to_csv(parsed_df, output_path)
