from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import os

# Load telemetry dataset once at startup
# Assume bundle is a local JSON file uploaded with repo
with open(os.path.join(os.path.dirname(__file__), "telemetry.json")) as f:
    telemetry = json.load(f)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Query(BaseModel):
    regions: list[str]
    threshold_ms: int

@app.post("/latency")
async def get_metrics(query: Query):
    results = {}
    
    for region in query.regions:
        records = telemetry.get(region, [])
        if not records:
            continue
        
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]  # assume uptime is a float %
        
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
