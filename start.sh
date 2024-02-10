#!/bin/bash

# Start Zookeeper
echo "Starting Zookeeper..."
/path/to/kafka/bin/zookeeper-server-start.sh /path/to/kafka/config/zookeeper.properties &

# Wait for Zookeeper to start
sleep 5

# Start Kafka server
echo "Starting Kafka server..."
/usr/bin/kafka/kafka-server-start.sh /usr/bin/kafka/config/server.properties &

# Wait for Kafka server to start
sleep 5

# Run Python script
echo "Running Python script..."
python3 ./app/main.py &

# Wait for Python script to start
sleep 5

# Submit Spark job
echo "Submitting Spark job..."
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /path/to/spark/SparkStream.py

echo "Data streaming is in progress..."