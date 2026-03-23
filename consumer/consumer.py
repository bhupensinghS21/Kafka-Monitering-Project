import time
from kafka import KafkaConsumer
import psycopg2, json

# Wait for Kafka
while True:
    try:
        consumer = KafkaConsumer(
            "logs",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset='earliest'
        )
        print("Connected to Kafka")
        break
    except Exception as e:
        print("Kafka not ready, retrying...", e)
        time.sleep(5)

# Wait for Postgres
while True:
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="logsdb",
            user="admin",
            password="admin"
        )
        print("Connected to Postgres")
        break
    except Exception as e:
        print("Postgres not ready, retrying...", e)
        time.sleep(5)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    level TEXT,
    service TEXT,
    message TEXT,
    timestamp FLOAT
)
""")
conn.commit()

print("Consumer started...")

for msg in consumer:
    data = msg.value

    cur.execute(
        "INSERT INTO logs (level, service, message, timestamp) VALUES (%s, %s, %s, %s)",
        (data["level"], data["service"], data["message"], data["timestamp"])
    )
    conn.commit()

    print("Inserted:", data)
