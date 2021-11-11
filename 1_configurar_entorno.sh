#!/bin/bash

sudo apt update

sudo apt-get -y install openjdk-8-jdk-headless

sudo apt -y install python

sudo apt -y install python3-pip

pip install kafka-python

cd ~

# SPARK

wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz

tar xvzf spark-2.3.0-bin-hadoop2.7.tgz

wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.1.1/kafka-clients-2.1.1.jar

wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.11/2.3.0/spark-sql-kafka-0-10_2.11-2.3.0.jar

cd ~

# KAFKA

wget https://archive.apache.org/dist/kafka/2.1.1/kafka_2.12-2.1.1.tgz --no-check-certificate

tar -xvf kafka_2.12-2.1.1.tgz

cd ~/kafka_2.12-2.1.1

nohup bin/zookeeper-server-start.sh config/zookeeper.properties & > /dev/null

nohup bin/kafka-server-start.sh config/server.properties & > /dev/null

cd ~
