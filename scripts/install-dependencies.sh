#!/bin/bash

# Path to the dependencies installed flag
dependencies_installed="$HOME/dependencies-installed-ok"

# Check if dependencies are already installed
if [ -e "$dependencies_installed" ]; then
    echo "Dependencies are already installed."
else
    # Update package lists
    echo "Updating package lists..."
    sudo apt-get update

    # Install Java Development Kit (JDK)
    echo "Installing Java Development Kit (JDK)..."
    sudo apt-get -y install default-jdk

    # Java version check
    java_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "Java version installed: $java_version"

    # Python versions
    python_version=3
    python_dev_package="python${python_version}-dev"
    python_pip_package="python${python_version}-pip"

    # Install Python and pip
    echo "Installing Python ${python_version} and pip..."
    sudo apt-get -y install "${python_dev_package}" "${python_pip_package}"

    # Kafka version
    kafka_version="3.6.1"
    kafka_scala_version="2.13"
    kafka_download_url="https://dlcdn.apache.org/kafka/${kafka_version}/kafka_${kafka_scala_version}-${kafka_version}.tgz"
    kafka_tar_file="kafka_${kafka_scala_version}-${kafka_version}.tgz"

    # Download Kafka to home directory
    echo "Downloading Kafka ${kafka_version}..."
    wget -P "$HOME" "${kafka_download_url}"

    # Extract Kafka archive in home directory
    echo "Extracting Kafka archive..."
    tar -xzf "$HOME/${kafka_tar_file}" -C "$HOME/"


    pip install pyspark

    # Mark dependencies as installed
    echo "Dependencies installed: ok" > "$dependencies_installed"
fi
