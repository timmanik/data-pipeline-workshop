# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all files
COPY . .

# Expose port for Flask
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]