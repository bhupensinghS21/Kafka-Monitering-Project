import time
from kafka import KafkaProducer
import json, random

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Connected to Kafka")
        break
    except Exception as e:
        print("Kafka not ready, retrying...", e)
        time.sleep(5)

events = ["INFO", "WARNING", "ERROR"]

print("Producer started...")

while True:
    log = {
        "level": random.choice(events),
        "service": "auth-service",
        "message": "Random log event",
        "timestamp": time.time()
    }

    producer.send("logs", log)
    print("Sent:", log)

    time.sleep(2)
