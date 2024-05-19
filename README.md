# Big Data Project: Real-Time Twitter Sentiment Analysis

## Overview

This repository contains a Big Data project focused on real-time sentiment analysis of Twitter data. The project leverages various technologies to collect, process, analyze, and visualize sentiment data from tweets in real-time.

## Project Architecture

The project is built using the following components:

- **Apache Kafka**: Used for real-time data ingestion from Twitter.
- **Spark Streaming**: Processes the streaming data from Kafka to perform sentiment analysis.
- **MongoDB**: Stores the processed sentiment data.
- **Django**: Serves as the web framework for building a real-time dashboard to visualize the sentiment analysis results.

- This is an img about the project :
   ![project img](imgs/flow.png)

## Features

- **Real-time Data Ingestion**: Collects live tweets using Kafka from the Twitter API.
- **Stream Processing**: Utilizes Spark Streaming to process and analyze the data in real-time.
- **Sentiment Analysis**: Classifies tweets into different sentiment categories (positive, negative, neutral) using natural language processing (NLP) techniques.
- **Data Storage**: Stores the sentiment analysis results in MongoDB for persistence.
- **Visualization**: Provides a real-time dashboard built with Django to visualize the sentiment trends and insights.

## Data description:
in This Project I'm using a Dataset (twitter_training.csv and twitter_validation.csv) to create pyspark Model.

Each line of the "twitter_training.csv" learning database represents a Tweet, it contains over 74682 lines;

The data types of Features are:
- Tweet ID: int
- Entity: string
- Sentiment: string (Target)
- Tweet content: string

The validation database “twitter_validation.csv” contains 998 lines (Tweets) with the same features of “twitter_training.csv”

This is the Data Source:
https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis

## Getting Started

### Prerequisites

To run this project, you will need the following installed on your system:

- Docker (for runing Kafka)
- Python 3.x
- Apache Kafka
- Apache Spark (PySpark for python)
- MongoDB
- Django

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/drisskhattabi6/Real-Time-Twitter-Sentiment-Analysis.git
   cd big-data-project
   ```
   
2. **Installing Docker Desktop**

3. **Set up Kafka**:
   - Download and install Apache Kafka in docker using :
   ```bash
   docker-compose -f zk-single-kafka-single.yml up -d
   ```

5. **Set up MongoDB**:
   - Download and install MongoDB.
   - Start the MongoDB server.
     - It is recommended to install **MongoDBCompass** to visualize data and makes working with mongodb easier.

6. **Install Python dependencies**:
   - To install pySpark - PyMongo - Django ...
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure Twitter API credentials**:
   - Obtain Twitter API keys and tokens.
   - Set them in your environment variables or a configuration file.

### Running the Project

1. **Start Kafka and create topics**:
   ```bash
   kafka-server-start.sh /path/to/kafka/config/server.properties
   kafka-topics.sh --create --topic twitter-stream --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

2. **Run the Spark Streaming application**:
   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /path/to/your/spark/application.py
   ```

3. **Start MongoDB**:
   ```bash
   mongod
   ```

4. **Run the Django server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the Dashboard**:
   Open your web browser and go to `http://127.0.0.1:8000` to view the real-time sentiment analysis dashboard.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact us at [your-email@example.com].

---

By following the above instructions, you should be able to set up and run the real-time Twitter sentiment analysis project on your local machine. Happy coding!
