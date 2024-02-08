FROM python:3.8-slim

# Install Kafka and Spark dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jre-headless wget && \
    wget -q wget https://downloads.apache.org/kafka/3.5.1/kafka_2.13-3.5.1.tgz && \
    tar -xzf kafka_2.13-3.5.1.tgz && \
    mv kafka_2.13-3.5.1 /opt/kafka && \
    rm kafka_2.13-3.5.1.tgz

# Install Apache Spark
RUN wget -q https://downloads.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz && \
    tar -xzf spark-3.2.0-bin-hadoop3.2.tgz && \
    mv spark-3.2.0-bin-hadoop3.2 /opt/spark && \
    rm spark-3.2.0-bin-hadoop3.2.tgz

# Install PySpark
RUN pip install pyspark

# Set environment variables for Kafka and Spark
ENV KAFKA_HOME /opt/kafka
ENV SPARK_HOME /opt/spark
ENV PATH $PATH:$SPARK_HOME/bin

# Set environment variables for the application
ENV KAFKA_BOOTSTRAP_SERVERS localhost:9092
ENV KAFKA_TOPIC topic_currency_exch_rate
ENV OUTPUT_PATH output_csv

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code into the container at /app
COPY . /app

# Start command to run  Spark application when the container starts
CMD ["./app/start.sh"]
