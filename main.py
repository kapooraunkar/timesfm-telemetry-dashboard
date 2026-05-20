from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import clickhouse_connect
import numpy as np
import timesfm

app = FastAPI()

# Allow frontend-backend communication

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect Python to ClickHouse

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password=""
)

# Load TimesFM model ONCE

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

@app.get("/metrics")
def get_metrics():

    query = """
    SELECT ram_usage, cpu_usage
    FROM metrics
    ORDER BY timestamp ASC
    LIMIT 120
    """

    result = client.query(query)

    rows = result.result_rows

    # First 100 points = historical context

    historical_ram = [
        row[0] for row in rows[:100]
    ]

    historical_cpu = [
        row[1] for row in rows[:100]
    ]

    # Next 20 points = actual future validation

    actual_future_ram = [
        row[0] for row in rows[100:120]
    ]

    actual_future_cpu = [
        row[1] for row in rows[100:120]
    ]

    # RAM forecasting

    ram_series = np.array(historical_ram)

    ram_forecast, _ = tfm.forecast(
        [ram_series]
    )

    forecast_ram = ram_forecast[0].tolist()

    # CPU forecasting

    cpu_series = np.array(historical_cpu)

    cpu_forecast, _ = tfm.forecast(
        [cpu_series]
    )

    forecast_cpu = cpu_forecast[0].tolist()

    return {

        "historical_ram": historical_ram,
        "forecast_ram": forecast_ram,
        "actual_future_ram": actual_future_ram,

        "historical_cpu": historical_cpu,
        "forecast_cpu": forecast_cpu,
        "actual_future_cpu": actual_future_cpu
    }