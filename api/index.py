from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

# Sample telemetry data (replace/add more records as needed)
telemetry = [
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 103.67,
    "uptime_pct": 99.269,
    "timestamp": 20250301
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 206.81,
    "uptime_pct": 98.88,
    "timestamp": 20250302
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 150.4,
    "uptime_pct": 97.798,
    "timestamp": 20250303
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 139.44,
    "uptime_pct": 97.891,
    "timestamp": 20250304
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 159.57,
    "uptime_pct": 97.519,
    "timestamp": 20250305
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 231.17,
    "uptime_pct": 97.365,
    "timestamp": 20250306
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 155.99,
    "uptime_pct": 97.822,
    "timestamp": 20250307
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 177.31,
    "uptime_pct": 97.575,
    "timestamp": 20250308
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 236.58,
    "uptime_pct": 97.27,
    "timestamp": 20250309
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 152.06,
    "uptime_pct": 98.879,
    "timestamp": 20250310
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 143.73,
    "uptime_pct": 98.738,
    "timestamp": 20250311
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 100.63,
    "uptime_pct": 98.563,
    "timestamp": 20250312
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 186.77,
    "uptime_pct": 97.498,
    "timestamp": 20250301
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 223.88,
    "uptime_pct": 99.071,
    "timestamp": 20250302
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 225.29,
    "uptime_pct": 98.303,
    "timestamp": 20250303
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 126.49,
    "uptime_pct": 97.432,
    "timestamp": 20250304
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 183.37,
    "uptime_pct": 99.029,
    "timestamp": 20250305
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 169.76,
    "uptime_pct": 98.48,
    "timestamp": 20250306
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 135.66,
    "uptime_pct": 97.909,
    "timestamp": 20250307
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 125.56,
    "uptime_pct": 97.164,
    "timestamp": 20250308
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 219.31,
    "uptime_pct": 97.868,
    "timestamp": 20250309
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 132,
    "uptime_pct": 99.2,
    "timestamp": 20250310
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 122.16,
    "uptime_pct": 98.539,
    "timestamp": 20250311
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 107.86,
    "uptime_pct": 98.703,
    "timestamp": 20250312
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 162.82,
    "uptime_pct": 98.083,
    "timestamp": 20250301
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 171.9,
    "uptime_pct": 97.271,
    "timestamp": 20250302
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 154.74,
    "uptime_pct": 98.954,
    "timestamp": 20250303
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 130.84,
    "uptime_pct": 98.581,
    "timestamp": 20250304
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 222.48,
    "uptime_pct": 98.746,
    "timestamp": 20250305
  },
  {
    "region": "amer",
    "service": "support",
    "latency_ms": 123.92,
    "uptime_pct": 99.387,
    "timestamp": 20250306
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 183.61,
    "uptime_pct": 99.035,
    "timestamp": 20250307
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 157.98,
    "uptime_pct": 99.103,
    "timestamp": 20250308
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 212.52,
    "uptime_pct": 98.047,
    "timestamp": 20250309
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 215.67,
    "uptime_pct": 99.02,
    "timestamp": 20250310
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 141.13,
    "uptime_pct": 99.242,
    "timestamp": 20250311
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 134.05,
    "uptime_pct": 98.826,
    "timestamp": 20250312
  }
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
