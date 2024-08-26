# Base image
FROM python:3.9-slim AS base
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Extract stage
FROM base AS extract
WORKDIR /usr/src/app
COPY scripts/extract.py ./
COPY entrypoints/extract.sh ./
RUN chmod +x extract.sh
ENTRYPOINT ["sh", "extract.sh"]

# Load stage
FROM base AS load
WORKDIR /usr/src/app
COPY scripts/load.py ./
COPY entrypoints/load.sh ./
RUN chmod +x load.sh
ENTRYPOINT ["sh", "load.sh"]

# Transform stage
FROM base AS transform
WORKDIR /usr/src/app
COPY scripts/transform.py ./
COPY entrypoints/transform.sh ./
RUN chmod +x transform.sh
ENTRYPOINT ["sh", "transform.sh"]