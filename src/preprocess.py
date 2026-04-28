import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json

class Preprocessor:
    def __init__(self, drop_cols=None):
        self.drop_cols = drop_cols if drop_cols is not None else []
        self.medians = {}
        self.label_encoders = {}
        self.freq_encoders = {}
        self.cat_cols = []
        self.num_cols = []
    
    def fit(self, df):
        # Identify drop columns if not provided (>85% null)
        if not self.drop_cols:
            missing_pct = df.isnull().mean() * 100
            self.drop_cols = missing_pct[missing_pct > 85].index.tolist()
            
        # Drop columns with 1 unique value (constant)
        for col in df.columns:
            if col not in self.drop_cols and df[col].nunique() <= 1:
                self.drop_cols.append(col)
                
        df_filtered = df.drop(columns=self.drop_cols, errors='ignore')
        
        # Identify numeric and categorical columns
        self.num_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = df_filtered.select_dtypes(exclude=[np.number]).columns.tolist()
        
        # Calculate medians for numeric
        for col in self.num_cols:
            self.medians[col] = df_filtered[col].median()
            
        # Fit encoders for categoricals
        for col in self.cat_cols:
            # High cardinality threshold
            if df_filtered[col].nunique() > 50:
                self.freq_encoders[col] = df_filtered[col].value_counts(normalize=True).to_dict()
            else:
                le = LabelEncoder()
                # Fill na with 'Unknown' before fitting
                le.fit(df_filtered[col].fillna('Unknown').astype(str))
                self.label_encoders[col] = le
                
        return self

    def transform(self, df):
        df_out = df.copy()
        
        # Drop columns
        df_out = df_out.drop(columns=self.drop_cols, errors='ignore')
        
        # Numeric Null Fill -> Median
        for col in self.num_cols:
            if col in df_out.columns:
                df_out[col] = df_out[col].fillna(self.medians.get(col, 0))
                
        # Categorical Null Fill & Encoding
        for col in self.cat_cols:
            if col in df_out.columns:
                df_out[col] = df_out[col].fillna('Unknown').astype(str)
                
                if col in self.freq_encoders:
                    # Frequency encoding
                    freq_map = self.freq_encoders[col]
                    df_out[col] = df_out[col].map(freq_map).fillna(0)
                elif col in self.label_encoders:
                    # Label encoding
                    le = self.label_encoders[col]
                    # Handle unseen labels
                    classes = set(le.classes_)
                    df_out[col] = df_out[col].map(lambda s: s if s in classes else 'Unknown')
                    # Refit might be needed for 'Unknown' if it wasn't in original, but safe approach is to just transform
                    # To avoid ValueError on unseen, we already handled it above if 'Unknown' was in classes
                    try:
                        df_out[col] = le.transform(df_out[col])
                    except ValueError:
                        # Fallback if 'Unknown' wasn't seen in train
                        pass
        return df_out
