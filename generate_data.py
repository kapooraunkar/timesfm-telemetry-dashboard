from faker import Faker
import clickhouse_connect

import math
import random
from datetime import datetime, timedelta

fake = Faker()

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="admin",
    password="admin123"
)

# Clear old data

client.command("TRUNCATE TABLE metrics")

rows = []

start_time = datetime.now()

for i in range(200):

    timestamp = start_time + timedelta(seconds=i * 5)

    # RAM pattern
    # gradual wave + slight noise

    ram = 70 + 10 * math.sin(i / 10) \
+ random.uniform(-2, 2)

    # CPU pattern
    # faster oscillation + spikes

    cpu = 40 + 20 * math.sin(i / 5) \
        + random.uniform(-5, 5)

    rows.append([
        timestamp,
        round(ram, 2),
        round(cpu, 2)
    ])

client.insert(
    "metrics",
    rows,
    column_names=[
        "timestamp",
        "ram_usage",
        "cpu_usage"
    ]
)

print("Synthetic telemetry inserted successfully.")