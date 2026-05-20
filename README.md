# Telemetry Forecast Validation Dashboard

A real-time telemetry forecasting dashboard built using:

- Go + gopsutil
- ClickHouse
- FastAPI
- TimesFM
- Chart.js

## Features

- Real-time RAM and CPU telemetry collection
- ClickHouse telemetry storage
- FastAPI backend APIs
- TimesFM-based forecasting
- Forecast validation against actual future telemetry
- Interactive visualization dashboard

## Forecasting Workflow

1. Historical telemetry is collected from ClickHouse
2. TimesFM predicts future telemetry points
3. Actual future telemetry is compared against predictions
4. Dashboard visualizes forecast validation

## Tech Stack

- Go
- ClickHouse
- FastAPI
- Python
- TimesFM
- Chart.js
- Docker