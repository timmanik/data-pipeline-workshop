#!/bin/bash
set -e

# Ensure /data directory exists
mkdir -p /data

# Wait for extract stage to complete
while [ ! -f /data/extract_done ]; do
echo "Waiting for extract stage to complete..."
sleep 5
done

# Run the load script
python /usr/src/app/load.py

# Signal successful completion
touch /data/load_done