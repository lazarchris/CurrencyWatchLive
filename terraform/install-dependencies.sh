#!/bin/bash

# Python versions
python_version=3
python_dev_package=python${python_version}-dev
python_pip_package=python${python_version}-pip

# Kafka version
kafka_version=3.6.1
kafka_scala_version=2.13
kafka_download_url="https://dlcdn.apache.org/kafka/${kafka_version}/kafka_${kafka_scala_version}-${kafka_version}.tgz"
kafka_tar_file="kafka_${kafka_scala_version}-${kafka_version}.tgz"
kafka_dir="kafka_${kafka_scala_version}-${kafka_version}"

echo "Updating package lists..."
sudo apt-get update

echo "Installing Python ${python_version} and pip..."
sudo apt-get -y install ${python_dev_package} ${python_pip_package}

echo "Downloading Kafka ${kafka_version}..."
wget ${kafka_download_url}

echo "Extracting Kafka archive..."
tar -xzf ${kafka_tar_file}

echo "Starting Zookeeper server..."
cd ${kafka_dir}
bin/zookeeper-server-start.sh config/zookeeper.properties &

echo "Starting Kafka server..."
bin/kafka-server-start.sh config/server.properties &
