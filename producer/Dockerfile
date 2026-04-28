FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY producer/ /app/producer/
COPY data/ /app/data/
COPY .env* /app/

CMD ["python", "producer/producer.py"]
