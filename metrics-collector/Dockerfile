# Dockerfile for Metrics Collector

# Python base image
FROM python:3.11-slim

# Create and set present working directory
WORKDIR /metrics-Collector

# Install iproute2, curl & ping
RUN apt-get update && apt-get install -y \
iproute2 \
curl \
iputils-ping \
&& rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt ./

# Install dependencies based on requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and dependencies
COPY . .

# Port Mapping
EXPOSE 6000

# Execute the app.py
CMD [ "python" , "app.py" ]
