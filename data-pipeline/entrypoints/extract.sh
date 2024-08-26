#!/bin/bash
set -e

# Ensure /data directory exists
mkdir -p /data

echo "Starting extract process..."
python /usr/src/app/extract.py

echo "Extract process completed."

# Signal successful completion
touch /data/extract_done