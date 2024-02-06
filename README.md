## CurrencyWatchLive

CurrencyWatchLive is a real-time currency exchange rate monitoring tool developed for data analytics projects. It provides a comprehensive solution for analyzing currency exchange rates using live data streams.

### Directory Structure

```
CurrencyWatchLive/
├── api
│   ├── CurrencyConverter.py
│   ├── KafkaConsumer.py
│   ├── KafkaProducer.py
│   ├── main.py
│   └── settings.json
├── Dockerfile
├── README.md
├── requirements.txt
├── spark
│   └── SparkStream.py
├── start.sh
└── terraform
    └── main.tf
```

### Components

- **api**: 
  - `CurrencyConverter.py`: Provides currency conversion functionality.
  - `KafkaConsumer.py`: Handles communication with Kafka for consuming data.
  - `KafkaProducer.py`: Handles communication with Kafka for producing data.
  - `main.py`: Main script for running the application.
  - `settings.json`: Stores configuration settings.

- **Dockerfile**: Defines instructions for building a Docker image for the project, facilitating easy deployment and containerization.

- **README.md**: This file. Provides an overview of the project, its components, and how to use it.

- **requirements.txt**: Lists Python dependencies required for running the project. Can be used with pip to install necessary packages.

- **spark**: Contains Spark-related scripts, with `SparkStream.py` likely being the main script for streaming currency exchange rate data using Apache Spark.

- **start.sh**: Shell script used to start the project or perform setup tasks. Can be used for running the application or setting up environment variables.

- **terraform**: Directory containing Terraform configuration files, particularly `main.tf`, which defines the infrastructure for deploying and managing the project on Azure.

### Usage

To use CurrencyWatchLive:

1. Ensure you have Python installed on your system.
2. Install project dependencies using `pip install -r requirements.txt`.
3. Configure settings in `api/settings.json` according to your requirements.
4. Run the application using `python api/main.py`.

Alternatively, you can build and deploy the Docker image using the provided Dockerfile.

### Contributing

If you'd like to contribute to CurrencyWatchLive, feel free to submit a pull request or open an issue on GitHub. We welcome contributions of all kinds, from bug fixes to new features and enhancements.

### License

CurrencyWatchLive is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.