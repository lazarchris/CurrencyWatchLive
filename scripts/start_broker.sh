#!/bin/bash
kafka_version="3.6.1"
kafka_scala_version="2.13"
kafka_dir="kafka_${kafka_scala_version}-${kafka_version}"

# Start Zookeeper server
echo "Starting Zookeeper server..."
cd "$HOME/${kafka_dir}" || exit
bin/zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka server
echo "Starting Kafka server..."
bin/kafka-server-start.sh config/server.properties &
