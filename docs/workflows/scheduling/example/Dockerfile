# start with a Python 3.13 base image
FROM python:3.13-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    git \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# set the workspace
WORKDIR /app

# install the DHIS2 Climate Tools environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt