#!/usr/bin/python 

import sys, time, json, random
from kafka import KafkaProducer


def generar_transaccion():
    x = {
        "cliente": random.randrange(1, 6),
        "importe": random.randrange(-500, 500, 50)
    }
    return x


def producir_en_kafka(data, topic):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"], 
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()


def main():
    topic = sys.argv[1]
    while True:
        data = generar_transaccion()
        print(data)
        producir_en_kafka(data, topic)
        time.sleep(random.randrange(1, 6))


if __name__ == "__main__":
    main()
