"""
Demo Spark Structured Streaming + Apache Kafka + Cassandra
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

import sys


def writeToCassandra(df, epochId):
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="transacciones", keyspace="demo") \
        .mode("append") \
        .save()


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
        .createOrReplaceTempView("tmp_table")

    query = """
        SELECT FROM_JSON(
                CAST(value AS STRING), 'cliente INT, importe INT'
            ) AS json_struct 
        FROM tmp_table
    """

    spark.sql(query) \
        .select("json_struct.*") \
        .groupBy("cliente").agg(sum("importe").alias("importe")) \
        .writeStream \
        .foreachBatch(writeToCassandra) \
        .outputMode("update") \
        .trigger(processingTime='10 seconds') \
        .start() \
        .awaitTermination()


if __name__ == "__main__":
    main()
