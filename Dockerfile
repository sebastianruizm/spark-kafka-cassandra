FROM ubuntu:20.04
LABEL maintainer="https://www.linkedin.com/in/sebastianruizmartinez/"
WORKDIR /spark-demo

ENV SPARK_HOME /spark-demo/spark
ENV KAFKA_HOME /spark-demo/kafka
ENV CASSANDRA_HOME /spark-demo/cassandra

RUN apt-get update
RUN apt-get install -y openjdk-8-jdk-headless wget python python3-pip
RUN pip install kafka-python

RUN mkdir scripts
COPY scripts scripts
RUN chmod 777 scripts/bash/setup-env.sh

# SPARK
RUN wget https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
RUN tar xvzf spark-2.4.3-bin-hadoop2.7.tgz
RUN rm spark-2.4.3-bin-hadoop2.7.tgz
RUN mv spark-2.4.3-bin-hadoop2.7 spark

ENV PATH=${PATH}:$SPARK_HOME/bin/

# KAFKA
RUN wget https://archive.apache.org/dist/kafka/2.1.1/kafka_2.12-2.1.1.tgz --no-check-certificate
RUN tar xvzf kafka_2.12-2.1.1.tgz
RUN rm kafka_2.12-2.1.1.tgz
RUN mv kafka_2.12-2.1.1 kafka

# CASSANDRA
RUN wget http://archive.apache.org/dist/cassandra/2.2.16/apache-cassandra-2.2.16-bin.tar.gz
RUN tar xzvf apache-cassandra-2.2.16-bin.tar.gz
RUN rm apache-cassandra-2.2.16-bin.tar.gz
RUN mv apache-cassandra-2.2.16 cassandra
