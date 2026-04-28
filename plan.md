# IEEE-CIS Fraud Detection Platform (FINAL OPTIMAL PLAN)
## Production-Grade Resume Project using XGBoost + Kafka + FastAPI + Docker + AWS

---

# 0. OBJECTIVE

Build a real-world fraud detection system using the IEEE-CIS Fraud Detection dataset with:

- Strong tabular ML model (XGBoost)
- Proper preprocessing for messy real data
- Real-time streaming simulation
- FastAPI prediction APIs
- Kafka producer/consumer architecture
- Dockerized services
- AWS deployment
- Clean GitHub-ready repo
- Resume-grade engineering quality

---

# 1. FINAL TECH STACK

## ML / Analytics
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Optuna
- SHAP
- Matplotlib

## Serving
- FastAPI
- Uvicorn

## Streaming
- Apache Kafka

## Infra
- Docker
- Docker Compose

## Cloud
- AWS EC2
- AWS S3
- AWS DynamoDB (optional)

## Notebook Work
- Google Colab (.ipynb preferred for heavy training)
- Local Jupyter optional

---

# 2. WHEN TO USE COLAB vs LOCAL

## Use Google Colab (.ipynb mandatory preferred)

### Heavy tasks:
- Loading full IEEE dataset
- EDA
- Feature engineering experiments
- Model training on full data
- Hyperparameter tuning
- SHAP generation

## Use Local Machine

### Engineering tasks:
- FastAPI
- Kafka producer
- Kafka consumer
- Docker Compose
- App integration
- GitHub repo work

## Final Rule

Training = Colab  
System engineering = Local

---

# 3. FINAL PROJECT STRUCTURE

fraud-detection/
│── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
│── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_train_xgboost.ipynb
│   ├── 04_optuna_tuning.ipynb
│   └── 05_shap_analysis.ipynb
│
│── model/
│   ├── fraud_model.pkl
│   ├── feature_columns.pkl
│   ├── encoders.pkl
│   ├── threshold.json
│   └── metadata.json
│
│── src/
│   ├── preprocess.py
│   ├── feature_builder.py
│   ├── predict.py
│   ├── schemas.py
│   └── utils.py
│
│── producer/
│   └── producer.py
│
│── consumer/
│   └── consumer.py
│
│── api/
│   └── main.py
│
│── reports/
│
│── tests/
│
│── docker-compose.yml
│── requirements.txt
│── README.md
│── .env.example

---

# 4. DATASET SOURCE

Use:

Kaggle → IEEE-CIS Fraud Detection

Files:

- train_transaction.csv
- train_identity.csv
- test_transaction.csv
- test_identity.csv

---

# 5. VERY IMPORTANT STRATEGY

DO NOT train immediately on full dataset.

Use this sequence:

## Phase A

100k sample rows

## Phase B

250k rows

## Phase C

Full train set

This saves time and prevents frustration.

---

# 6. COMPLETE EXECUTION ROADMAP

# PHASE 1 — DOWNLOAD + LOAD DATA (Colab .ipynb)

Create:

notebooks/01_eda.ipynb

Tasks:

- upload Kaggle API key
- download dataset
- unzip
- load CSVs
- inspect shapes
- merge transaction + identity on TransactionID

Output:

merged dataframe

---

# PHASE 2 — DATA AUDIT (Colab)

Check:

- missing values %
- duplicate rows
- target distribution
- column types
- memory usage
- leakage suspicion columns

Output:

clean column strategy list

---

# PHASE 3 — PREPROCESSING PLAN

Create src/preprocess.py

Rules:

## Drop Columns

- >85% null columns
- useless IDs if no signal
- constant columns

## Numeric Null Fill

median

## Categorical Null Fill

"Unknown"

## Encode Categoricals

Preferred:

Label Encoding for XGBoost

Large cardinality columns:

frequency encoding

---

# PHASE 4 — FEATURE ENGINEERING (Colab .ipynb)

Create:

notebooks/02_feature_engineering.ipynb

Build:

- transaction_hour
- transaction_day
- transaction_weekday
- email_domain_match
- amount_log
- amount_per_card_mean
- card_velocity_count
- device_risk_score
- addr_mismatch_flag
- browser_risk_group
- user_transaction_count

Important:

No future leakage.

Save final selected columns.

---

# PHASE 5 — TRAIN MODEL (Colab .ipynb)

Create:

notebooks/03_train_xgboost.ipynb

Train:

XGBClassifier

Use:

- train / validation split
- stratify target
- early stopping
- eval_set

Suggested start params:

n_estimators=1000
learning_rate=0.03
max_depth=7
subsample=0.8
colsample_bytree=0.8
scale_pos_weight=fraud imbalance ratio

Metrics:

- ROC AUC
- PR AUC
- Precision
- Recall
- F1
- Confusion Matrix

Target realistic result:

ROC-AUC 0.90+

---

# PHASE 6 — TUNING (Colab .ipynb)

Create:

notebooks/04_optuna_tuning.ipynb

Tune:

- max_depth
- min_child_weight
- gamma
- reg_alpha
- reg_lambda
- eta
- subsample

Run 30–50 trials only.

Save best params.

---

# PHASE 7 — EXPLAINABILITY (Colab .ipynb)

Create:

notebooks/05_shap_analysis.ipynb

Generate:

- feature importance
- SHAP summary
- waterfall sample predictions

Save charts in reports/

---

# PHASE 8 — EXPORT ARTIFACTS

Save:

model/fraud_model.pkl  
model/feature_columns.pkl  
model/encoders.pkl  
model/threshold.json  
model/metadata.json

threshold.json:

{
 "fraud_threshold": 0.72
}

---

# PHASE 9 — LOCAL INFERENCE ENGINEERING

Create:

src/predict.py

Responsibilities:

- load model
- load encoders
- align columns
- predict probability
- return score + label

Must work in <200ms local request.

---

# PHASE 10 — FASTAPI

Create:

api/main.py

Endpoints:

GET /health

POST /predict

POST /batch_predict

GET /model_info

GET /stats

Example POST:

{
 "TransactionAmt": 1200,
 "ProductCD": "W",
 "card4": "visa",
 "DeviceType": "desktop"
}

Response:

{
 "fraud_probability": 0.81,
 "label": "fraud"
}

---

# PHASE 11 — STREAMING SYSTEM

# Producer

Create:

producer/producer.py

Read sample rows from processed CSV.

Every second send one event to Kafka topic:

transactions

# Consumer

Create:

consumer/consumer.py

Flow:

- consume event
- preprocess
- score model
- log result
- if fraud → store alert

---

# PHASE 12 — STORAGE

Simple version:

alerts.jsonl

Better version:

AWS DynamoDB table:

fraud_alerts

Fields:

- transaction_id
- score
- label
- timestamp

---

# PHASE 13 — DOCKERIZE

docker-compose.yml services:

- zookeeper (optional)
- kafka
- api
- producer
- consumer

Use healthchecks.

---

# PHASE 14 — AWS DEPLOYMENT

Use EC2 free tier.

Deploy:

- Docker Compose stack

Use S3:

- backup model
- reports
- logs archive

Optional:

CloudWatch logs

---

# PHASE 15 — TESTING

Create tests/

Test:

- preprocess output schema
- prediction endpoint
- missing value payload
- invalid categorical input
- consumer scoring path

---

# PHASE 16 — README (VERY IMPORTANT)

Include:

- architecture diagram
- dataset source
- metrics screenshots
- API screenshots
- docker run steps
- AWS deployment steps
- resume bullets

---

# 17. WHAT SCRIPTS SHOULD BE .IPYNB

MANDATORY NOTEBOOKS:

- 01_eda.ipynb
- 02_feature_engineering.ipynb
- 03_train_xgboost.ipynb
- 04_optuna_tuning.ipynb
- 05_shap_analysis.ipynb

Reason:

Better for Colab GPU/RAM + visuals.

---

# 18. WHAT SHOULD BE .PY FILES

Production code:

- preprocess.py
- predict.py
- main.py
- producer.py
- consumer.py

---

# 19. FINAL PERFORMANCE TARGET

Believable metrics:

ROC-AUC: 0.91–0.96  
PR-AUC: strong  
Recall: 75%+  
Precision: 70%+ depending threshold

Do NOT chase fake 100%.

---

# 20. RESUME BULLETS

- Built production-grade fraud detection platform using IEEE-CIS dataset (590k+ transactions) with XGBoost and streaming inference architecture.
- Designed preprocessing pipeline for high-missing, high-cardinality tabular fraud data.
- Implemented Kafka producer/consumer real-time scoring system with FastAPI APIs.
- Dockerized services and deployed on AWS EC2.

---

# 21. INTERVIEW QUESTIONS TO PREPARE

1. Why XGBoost over neural networks?
2. How did you handle missing values?
3. Why PR-AUC important in fraud?
4. How did you avoid leakage?
5. Why Kafka?
6. How to scale consumer group?
7. Why threshold not 0.5?
8. How to monitor drift?

---

# 22. IMPORTANT FINAL RULES

- Keep notebooks clean.
- Convert repeated notebook logic into src/*.py reusable modules.
- Never hardcode paths.
- Use .env.
- Keep logs structured.
- Keep code production style.

---

# 23. EXACT BUILD ORDER

1. Download data
2. EDA notebook
3. Feature engineering notebook
4. Train notebook
5. Tune notebook
6. Export model
7. Build predict.py
8. Build FastAPI
9. Build Kafka producer
10. Build Kafka consumer
11. Docker Compose
12. AWS deploy
13. README polish

---

# 24. FINAL COMMAND TO AI AGENT

Generate each file one by one with clean production-grade code.
Prefer .ipynb for training workflows.
Prefer modular reusable Python for deployment workflows.
Do not generate toy code.
Use enterprise coding standards.