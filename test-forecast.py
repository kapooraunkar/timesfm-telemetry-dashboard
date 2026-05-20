import clickhouse_connect
import numpy as np
import timesfm

# Connect to ClickHouse

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password=""
)

# Fetch historical RAM telemetry

query = """
SELECT ram_usage
FROM metrics
ORDER BY timestamp ASC
LIMIT 100
"""

result = client.query(query)

rows = result.result_rows

# Convert rows into simple array

data = [row[0] for row in rows]

series = np.array(data)

print("Historical Data:")
print(series)

# Load TimesFM model

tfm = timesfm.TimesFm(

    hparams=timesfm.TimesFmHparams(
        backend="cpu",
        per_core_batch_size=32,
        horizon_len=20,
    ),

    checkpoint=timesfm.TimesFmCheckpoint(
        huggingface_repo_id=
        "google/timesfm-1.0-200m-pytorch"
    ),
)

# Generate forecast

forecast, _ = tfm.forecast([series])

print("\nForecasted Values:")
print(forecast[0])