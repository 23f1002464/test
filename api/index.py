from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

# Sample telemetry data (replace with your real data)
telemetry = [
    {"region": "apac", "service": "catalog", "latency_ms": 103.67, "uptime_pct": 99.269, "timestamp": 20250301},
    {"region": "apac", "service": "support", "latency_ms": 206.81, "uptime_pct": 98.88, "timestamp": 20250302}
]

# Organize data per region
region_data = {}
for record in telemetry:
    region = record["region"]
    region_data.setdefault(region, []).append(record)

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Query(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.post("/latency")
async def get_latency(query: Query):
    results = {}
    for region in query.regions:
        records = region_data.get(region, [])
        if not records:
            results[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0
            }
            continue

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for l in latencies if l > query.threshold_ms)

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }

    return results
