#!/usr/bin/python 

import argparse
import json
import random
import sys
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

def main():
    parser = argparse.ArgumentParser(description="Produce random banking events to Kafka.")
    parser.add_argument("topic", help="Kafka topic to produce events to")
    parser.add_argument("--bootstrap-server", default="localhost:9092", help="Kafka bootstrap server (default: localhost:9092)")
    parser.add_argument("--num-events", type=int, default=10, help="Number of events to produce (default: 10)")
    args = parser.parse_args()

    try:
        producer = KafkaProducer(
            bootstrap_servers=args.bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    except KafkaError as e:
        print(f"Failed to connect to Kafka: {e}")
        return

    try:
        for _ in range(args.num_events):
            event = {
                "client": random.randint(1, 5),
                "amount": random.randint(-500, 500)
            }
            try:
                producer.send(args.topic, event)
                print(event)
            except KafkaError as e:
                print(f"Failed to send event: {e}")
            time.sleep(0.5)
    finally:
        producer.close()

if __name__ == "__main__":
    main()
