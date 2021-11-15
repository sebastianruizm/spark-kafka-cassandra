#!/bin/bash

sudo apt update

sudo apt-get -y install openjdk-8-jdk-headless

sudo apt -y install python

sudo apt -y install python3-pip

pip install kafka-python

cd ~

# SPARK

# Upgrade de versión para soportar foreachBatch (necesario para insert en Cassandra)
wget https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz

tar xvzf spark-2.4.3-bin-hadoop2.7.tgz

cd ~

# KAFKA

wget https://archive.apache.org/dist/kafka/2.1.1/kafka_2.12-2.1.1.tgz --no-check-certificate

tar -xvf kafka_2.12-2.1.1.tgz

cd ~/kafka_2.12-2.1.1

nohup bin/zookeeper-server-start.sh config/zookeeper.properties & > /dev/null

nohup bin/kafka-server-start.sh config/server.properties & > /dev/null

cd ~

# CASSANDRA

wget http://archive.apache.org/dist/cassandra/2.2.16/apache-cassandra-2.2.16-bin.tar.gz

tar xzvf apache-cassandra-2.2.16-bin.tar.gz

nohup ./apache-cassandra-2.2.16/bin/cassandra & > /dev/null

cd ~

cat << EOF > crear_tabla_transacciones.cql
CREATE KEYSPACE IF NOT EXISTS demo 
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
};
	
CREATE TABLE IF NOT EXISTS demo.transacciones (
   cliente int,
   importe int,
   PRIMARY KEY (cliente)
);

EOF

./apache-cassandra-2.2.16/bin/cqlsh -f crear_tabla_transacciones.cql

cd ~
