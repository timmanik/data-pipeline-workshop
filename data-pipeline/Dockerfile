# Base image - using slim for reduced attack surface
FROM python:3.13-alpine3.22 AS base

# Create non-root user for security
RUN addgroup -S appuser && adduser -S -G appuser appuser

WORKDIR /usr/src/app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create /data directory with proper permissions
RUN mkdir -p /data && chown -R appuser:appuser /data

# Change ownership of the working directory
RUN chown -R appuser:appuser /usr/src/app

# Extract stage
FROM base AS extract
WORKDIR /usr/src/app

# Copy application files
COPY scripts/extract.py ./
COPY entrypoints/extract.sh ./

# Set secure permissions and switch to non-root user
RUN chmod +x extract.sh && \
    chown -R appuser:appuser /usr/src/app
USER appuser

ENTRYPOINT ["sh", "extract.sh"]

# Load stage  
FROM base AS load
WORKDIR /usr/src/app

COPY scripts/load.py ./
COPY entrypoints/load.sh ./

# Set secure permissions and switch to non-root user
RUN chmod +x load.sh && \
    chown -R appuser:appuser /usr/src/app
USER appuser

ENTRYPOINT ["sh", "load.sh"]

# Transform stage
FROM base AS transform
WORKDIR /usr/src/app

COPY scripts/transform.py ./
COPY entrypoints/transform.sh ./

# Set secure permissions and switch to non-root user
RUN chmod +x transform.sh && \
    chown -R appuser:appuser /usr/src/app
USER appuser

ENTRYPOINT ["sh", "transform.sh"]