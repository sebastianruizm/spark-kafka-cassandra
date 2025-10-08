"""
Demo Spark Structured Streaming + Apache Kafka + Cassandra

Required Spark packages:
  --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3,org.apache.kafka:kafka-clients:2.1.1,com.datastax.spark:spark-cassandra-connector_2.11:2.4.3

Cassandra connection settings can be set via environment variables:
  CASSANDRA_HOST (default: 'localhost')
  CASSANDRA_PORT (default: '9042')
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col
from pyspark.sql.types import StructType, StructField, IntegerType
from pyspark.sql.utils import StreamingQueryException
from kafka import KafkaConsumer
import socket
import sys
import os

def check_kafka_connection(bootstrap_servers, topic):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            consumer_timeout_ms=1000
        )
        consumer.close()
    except Exception as e:
        print(f"[ERROR] Could not connect to Kafka at {bootstrap_servers}: {e}")
        sys.exit(1)

def check_cassandra_connection(host, port):
    try:
        with socket.create_connection((host, int(port)), timeout=2):
            pass
    except Exception as e:
        print(f"[ERROR] Could not connect to Cassandra at {host}:{port}: {e}")
        sys.exit(1)

def writeToCassandra(df, epochId):
    cassandra_host = os.getenv("CASSANDRA_HOST", "localhost")
    cassandra_port = os.getenv("CASSANDRA_PORT", "9042")
    try:
        df.write \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="transactions", keyspace="demo") \
            .option("spark.cassandra.connection.host", cassandra_host) \
            .option("spark.cassandra.connection.port", cassandra_port) \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"[ERROR] Failed to write to Cassandra: {e}")

def main():
    spark = SparkSession.builder \
        .appName("Spark-Kafka-Cassandra") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    topic = sys.argv[1]
    kafka_bootstrap = "localhost:9092"
    cassandra_host = os.getenv("CASSANDRA_HOST", "localhost")
    cassandra_port = os.getenv("CASSANDRA_PORT", "9042")

    # Check service connections before starting streaming
    check_kafka_connection(kafka_bootstrap, topic)
    check_cassandra_connection(cassandra_host, cassandra_port)

    # Define schema for validation
    schema = StructType([
        StructField("client", IntegerType(), True),
        StructField("amount", IntegerType(), True)
    ])

    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse and validate JSON messages
    parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
        .selectExpr("FROM_JSON(json_str, '{}') as data".format(schema.json())) \
        .select("data.*") \
        .filter(col("client").isNotNull() & col("amount").isNotNull())

    # Optionally log malformed messages
    malformed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
        .selectExpr("FROM_JSON(json_str, '{}') as data".format(schema.json())) \
        .filter(col("data.client").isNull() | col("data.amount").isNull())
    malformed_query = malformed_df.writeStream \
        .format("console") \
        .option("truncate", False) \
        .outputMode("append") \
        .start()

    try:
        parsed_df \
            .groupBy("client").agg(sum("amount").alias("amount")) \
            .writeStream \
            .foreachBatch(writeToCassandra) \
            .outputMode("update") \
            .trigger(processingTime='10 seconds') \
            .start() \
            .awaitTermination()
    except StreamingQueryException as e:
        print(f"[ERROR] Streaming query failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
