# Base Image
FROM python:3.10-slim

#System working Directory
WORKDIR /bulkhead-bot-backend

# Environment Optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
# Execute Package Installation
COPY ./requirements.txt /bulkhead-bot-backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bulkhead-bot-backend/requirements.txt

# Copy application files
COPY . /bulkhead-bot-backend