# Use the latest Alpine for security patches
FROM python:3.13-alpine3.22

# Install security updates and build dependencies
RUN apk update && apk upgrade && apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    freetype-dev \
    libpng-dev \
    jpeg-dev \
    zlib-dev \
    pkgconfig \
    python3-dev \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -S appuser && adduser -S appuser -G appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies with latest versions
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy application code and set ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Use non-privileged port
EXPOSE 8080

# Run Flask app with exec form
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]