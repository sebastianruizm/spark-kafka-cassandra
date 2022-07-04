#!/usr/bin/python 

import sys, time, json, random
from kafka import KafkaProducer

def generate_random_event():
    x = {
        "client": random.randrange(1, 6),
        "amount": random.randrange(-500, 500, 50)
    }
    return x

def produce_to_kafka(data, topic):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"], 
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()

def main():
    topic = sys.argv[1]
    while True:
        data = generate_random_event()
        print(data)
        produce_to_kafka(data, topic)
        time.sleep(random.randrange(1, 6))

if __name__ == "__main__":
    main()
