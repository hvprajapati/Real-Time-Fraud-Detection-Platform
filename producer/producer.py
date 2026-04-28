import os
import json
import time
import pandas as pd
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
KAFKA_BROKER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def create_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def main():
    print(f"Connecting to Kafka at {KAFKA_BROKER}")
    producer = create_producer()
    
    # Read sample data (we can use the raw train dataset or a smaller sample)
    data_path = os.path.join(os.path.dirname(__file__), '../data/raw/train_transaction.csv')
    
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}. Please download the dataset first.")
        return
        
    print(f"Loading data from {data_path}...")
    # Load just a chunk to stream
    df = pd.read_csv(data_path, nrows=1000)
    
    # Simulate streaming
    print("Starting stream...")
    for idx, row in df.iterrows():
        # Replace NaNs with None for JSON serialization
        record = row.where(pd.notnull(row), None).to_dict()
        
        producer.send('transactions', value=record)
        print(f"Sent TransactionID: {record.get('TransactionID')}")
        
        time.sleep(1) # Send every 1 second

if __name__ == "__main__":
    main()
