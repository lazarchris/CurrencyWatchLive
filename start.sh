#!/bin/bash

# Start Zookeeper
echo "Starting Zookeeper..."
/path/to/kafka/bin/zookeeper-server-start.sh /path/to/kafka/config/zookeeper.properties &

# Wait for Zookeeper to start
sleep 5

# Start Kafka server
echo "Starting Kafka server..."
/path/to/kafka/bin/kafka-server-start.sh /path/to/kafka/config/server.properties &

# Wait for Kafka server to start
sleep 5

# Run Python script
echo "Running Python script..."
python /path/to/api/main.py &

# Wait for Python script to start
sleep 5

# Submit Spark job
echo "Submitting Spark job..."
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /path/to/spark/CurrencyStrengthStream.py

echo "Data streaming is in progress..."