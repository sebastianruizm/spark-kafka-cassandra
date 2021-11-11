# Meetup Apache Spark México

Demo Spark Structured Streaming + Apache Kafka

## Entorno

AWS EC2 t2.large (Ubuntu Server 20.04 LTS)

```Shell
./1_configurar_entorno.sh 
```

## Kafka

Crear topic

```Shell
./kafka_2.12-2.1.1/bin/kafka-topics.sh \
--create \
--zookeeper localhost:2181 \
--replication-factor 1 \
--partitions 1 \
--topic topic_transacciones
```

Consumir mensajes de un topic

```Shell
./kafka_2.12-2.1.1/bin/kafka-console-consumer.sh \
--bootstrap-server localhost:9092 \
--topic topic_transacciones \
--from-beginning
```

## Python

Generar transacciones

```Shell
python3 2_generar_transacciones.py topic_transacciones
```

## Spark

Ejecutar aplicación streaming

```Shell
./spark-2.3.0-bin-hadoop2.7/bin/spark-submit \
--jars spark-sql-kafka-0-10_2.11-2.3.0.jar,kafka-clients-2.1.1.jar \
3_spark_streaming_kafka.py \
topic_transacciones
```


## Dependencias

- [kafka-python](https://kafka-python.readthedocs.io/en/master/)
- [kafka-clients-2.1.1](https://mvnrepository.com/artifact/org.apache.kafka/kafka-clients/2.1.1)
- [spark-sql-kafka-0-10_2.11-2.3.0](https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.11/2.3.0)
