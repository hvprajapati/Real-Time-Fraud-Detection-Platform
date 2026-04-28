FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY consumer/ /app/consumer/
COPY src/ /app/src/
COPY model/ /app/model/
COPY reports/ /app/reports/
COPY .env* /app/

CMD ["python", "consumer/consumer.py"]
