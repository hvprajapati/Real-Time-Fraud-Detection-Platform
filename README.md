# IEEE-CIS Fraud Detection Platform

## Production-Grade Resume Project using XGBoost + Kafka + FastAPI + Docker + AWS

### Architecture
![Architecture](reports/architecture_diagram.png)

### Dataset
This project uses the [IEEE-CIS Fraud Detection dataset](https://www.kaggle.com/c/ieee-fraud-detection).
It contains over 590k transactions with a heavily imbalanced fraud target.

### Quick Start

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. **Download Data**
   Use Kaggle API or download manually into `data/raw/`.
   Alternatively, run the `notebooks/01_eda.ipynb` to download and extract the data automatically.

3. **Train Models**
   Run the notebooks in `notebooks/` in order (1 to 5).
   The models and encoders will be saved to `model/`.

4. **Run via Docker Compose**
   ```bash
   docker-compose up --build
   ```
   This will spin up Zookeeper, Kafka, the FastAPI server, the Kafka Producer, and the Kafka Consumer.

### Metrics
ROC-AUC: ~0.90+
*(Screenshots of metrics and SHAP summary plots will be available in the `reports/` folder after running the notebooks).*

### AWS Deployment
1. Provision an EC2 instance (Amazon Linux 2 or Ubuntu).
2. Install Docker and Docker Compose.
3. Clone this repository.
4. Download the dataset and models (e.g., from S3).
5. Run `docker-compose up -d`.

### Resume Bullets
- Built production-grade fraud detection platform using IEEE-CIS dataset (590k+ transactions) with XGBoost and streaming inference architecture.
- Designed preprocessing pipeline for high-missing, high-cardinality tabular fraud data.
- Implemented Kafka producer/consumer real-time scoring system with FastAPI APIs.
- Dockerized services and deployed on AWS EC2.
