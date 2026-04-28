from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import time
from src.predict import get_predictor
import os
import json

app = FastAPI(title="Fraud Detection API")

class PredictRequest(BaseModel):
    # Dynamic payload to accept any feature dict
    data: Dict[str, Any]

class BatchPredictRequest(BaseModel):
    data: List[Dict[str, Any]]

@app.on_event("startup")
def load_model():
    # Warm up the predictor
    get_predictor()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(request: PredictRequest):
    try:
        predictor = get_predictor()
        start_time = time.time()
        result = predictor.predict(request.data)
        latency = (time.time() - start_time) * 1000
        result['latency_ms'] = round(latency, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch_predict")
def batch_predict(request: BatchPredictRequest):
    try:
        predictor = get_predictor()
        start_time = time.time()
        
        # This naive loop could be optimized to pass a dataframe for true batching
        results = [predictor.predict(row) for row in request.data]
        
        latency = (time.time() - start_time) * 1000
        return {
            "results": results,
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model_info")
def model_info():
    model_dir = os.path.join(os.path.dirname(__file__), '../model')
    try:
        with open(os.path.join(model_dir, 'metadata.json'), 'r') as f:
            metadata = json.load(f)
        with open(os.path.join(model_dir, 'threshold.json'), 'r') as f:
            threshold = json.load(f)
            
        return {**metadata, **threshold}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Model metadata not found")

@app.get("/stats")
def stats():
    # In a real app, you would connect to a DB or Redis to return real stats
    return {
        "total_requests": 0,
        "fraud_detected": 0
    }
