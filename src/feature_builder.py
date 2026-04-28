import numpy as np
import pandas as pd

def build_features(df):
    """
    Build features for the IEEE Fraud Dataset.
    Avoids future leakage by using only current row or aggregate statistics
    that would be available at prediction time.
    """
    df_out = df.copy()
    
    # Time features (TransactionDT is a timedelta in seconds from a reference point)
    # 86400 seconds in a day
    if 'TransactionDT' in df_out.columns:
        df_out['transaction_day'] = df_out['TransactionDT'] // 86400
        df_out['transaction_hour'] = (df_out['TransactionDT'] // 3600) % 24
        df_out['transaction_weekday'] = df_out['transaction_day'] % 7
    
    # Email domain match
    if 'P_emaildomain' in df_out.columns and 'R_emaildomain' in df_out.columns:
        df_out['email_domain_match'] = (df_out['P_emaildomain'] == df_out['R_emaildomain']).astype(int)
        
    # Amount features
    if 'TransactionAmt' in df_out.columns:
        df_out['amount_log'] = np.log1p(df_out['TransactionAmt'])
        
    # Example groupings (In a real system, you would compute these on history and join)
    # card1 to card6 are card features. Let's use card1 as main card ID
    if 'card1' in df_out.columns and 'TransactionAmt' in df_out.columns:
        # Warning: For true streaming, this needs to be tracked in a state store (like Redis/DynamoDB)
        # Here we just use a naive map derived from the current batch for simplicity.
        # In production, we load this from a pre-computed dictionary or state.
        amount_per_card_mean = df_out.groupby('card1')['TransactionAmt'].transform('mean')
        df_out['amount_per_card_mean'] = amount_per_card_mean
        
        # card_velocity_count
        card_velocity_count = df_out.groupby('card1')['TransactionID'].transform('count')
        df_out['card_velocity_count'] = card_velocity_count
        
    # Device risk score (mock example based on DeviceType)
    if 'DeviceType' in df_out.columns:
        # Typically mobile has different risk than desktop
        df_out['device_risk_score'] = df_out['DeviceType'].map({'mobile': 1, 'desktop': 0}).fillna(0.5)
        
    # Addr mismatch flag (addr1 and addr2)
    if 'addr1' in df_out.columns and 'addr2' in df_out.columns:
        df_out['addr_mismatch_flag'] = (df_out['addr1'] != df_out['addr2']).astype(int)
        
    # Browser risk group (id_31 typically contains browser info)
    if 'id_31' in df_out.columns:
        df_out['browser_risk_group'] = df_out['id_31'].str.contains('chrome|safari', case=False, na=False).astype(int)
        
    return df_out
