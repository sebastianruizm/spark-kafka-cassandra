FROM mcr.microsoft.com/devcontainers/python:3.10

# Install Java (required for Spark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

# Install Spark
ENV SPARK_VERSION=3.5.1
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt/ && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=$PATH:$SPARK_HOME/bin

# Install Kafka (optional, for local dev)
RUN apt-get install -y default-jre-headless && \
    wget https://archive.apache.org/dist/kafka/3.6.0/kafka_2.13-3.6.0.tgz && \
    tar xzf kafka_2.13-3.6.0.tgz -C /opt/ && \
    rm kafka_2.13-3.6.0.tgz
ENV KAFKA_HOME=/opt/kafka_2.13-3.6.0
ENV PATH=$PATH:$KAFKA_HOME/bin

# Install Cassandra (optional, for local dev)
RUN apt-get install -y cassandra

# Set JAVA_HOME for Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
