"""
Meetup Apache Spark Mexico
Demo Spark Structured Streaming + Apache Kafka
"""

from pyspark.sql import SparkSession
import sys


def main():
    spark = SparkSession.builder \
        .appName("Meetup-Apache-Spark-Mexico") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    topic = sys.argv[1]

    spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load() \
        .createOrReplaceTempView("tmp_topic_transacciones")

    query = """
        SELECT FROM_JSON(
                CAST(value AS STRING), 'cliente INT, importe INT'
            ) AS json_struct 
        FROM tmp_topic_transacciones
    """

    spark.sql(query) \
        .select("json_struct.*").groupBy("cliente").sum("importe") \
        .writeStream \
        .outputMode('complete') \
        .format('console') \
        .trigger(processingTime='10 seconds') \
        .start() \
        .awaitTermination()


if __name__ == "__main__":
    main()
