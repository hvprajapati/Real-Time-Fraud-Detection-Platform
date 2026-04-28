import os
import json
import time
from kafka import KafkaConsumer
from dotenv import load_dotenv
import sys

# Ensure src is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.predict import get_predictor

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
KAFKA_BROKER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def create_consumer():
    return KafkaConsumer(
        'transactions',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='fraud_detection_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def main():
    print(f"Initializing predictor...")
    try:
        predictor = get_predictor()
    except FileNotFoundError:
        print("Models not found. Train the models using the notebooks first.")
        return

    print(f"Connecting to Kafka consumer at {KAFKA_BROKER}")
    consumer = create_consumer()
    
    alerts_file = os.path.join(os.path.dirname(__file__), '../reports/alerts.jsonl')
    os.makedirs(os.path.dirname(alerts_file), exist_ok=True)
    
    print("Listening for transactions...")
    for message in consumer:
        record = message.value
        transaction_id = record.get('TransactionID', 'UNKNOWN')
        
        try:
            start_time = time.time()
            result = predictor.predict(record)
            latency = (time.time() - start_time) * 1000
            
            log_msg = f"Txn: {transaction_id} | Score: {result['fraud_probability']:.4f} | Label: {result['label']} | Time: {latency:.2f}ms"
            print(log_msg)
            
            # If fraud, save to alerts.jsonl (Phase 12)
            if result['label'] == 'fraud':
                alert = {
                    "transaction_id": transaction_id,
                    "score": result['fraud_probability'],
                    "label": result['label'],
                    "timestamp": time.time()
                }
                with open(alerts_file, 'a') as f:
                    f.write(json.dumps(alert) + '\n')
                    
        except Exception as e:
            print(f"Error processing Txn {transaction_id}: {e}")

if __name__ == "__main__":
    main()
