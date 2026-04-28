import pickle
import json
import os
import pandas as pd
import numpy as np

# Adjust paths to assume running from project root
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../model')

class FraudPredictor:
    def __init__(self):
        with open(os.path.join(MODEL_DIR, 'fraud_model.pkl'), 'rb') as f:
            self.model = pickle.load(f)
            
        with open(os.path.join(MODEL_DIR, 'encoders.pkl'), 'rb') as f:
            self.preprocessor = pickle.load(f)
            
        with open(os.path.join(MODEL_DIR, 'feature_columns.pkl'), 'rb') as f:
            self.feature_columns = pickle.load(f)
            
        with open(os.path.join(MODEL_DIR, 'threshold.json'), 'r') as f:
            self.threshold = json.load(f)['fraud_threshold']
            
    def predict(self, input_dict):
        # Convert to DataFrame
        df = pd.DataFrame([input_dict])
        
        # In a real scenario, we might need to apply feature_builder first.
        # But we assume the API gets raw rows and applies feature_builder
        from .feature_builder import build_features
        df = build_features(df)
        
        # Preprocess
        df_processed = self.preprocessor.transform(df)
        
        # Align columns
        # Add missing columns with 0
        for col in self.feature_columns:
            if col not in df_processed.columns:
                df_processed[col] = 0
                
        # Keep only required columns in order
        df_final = df_processed[self.feature_columns]
        
        # Predict probability
        prob = float(self.model.predict_proba(df_final)[0, 1])
        
        label = "fraud" if prob >= self.threshold else "legit"
        
        return {
            "fraud_probability": prob,
            "label": label
        }

# Singleton instance
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = FraudPredictor()
    return _predictor
