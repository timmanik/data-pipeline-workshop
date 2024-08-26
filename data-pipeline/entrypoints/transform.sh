#!/bin/bash
set -e

# Ensure /data directory exists
mkdir -p /data

# Wait for load stage to complete
while [ ! -f /data/load_done ]; do
echo "Waiting for load stage to complete..."
sleep 5
done

# Run the transform script
python /usr/src/app/transform.py

# Signal successful completion
touch /data/transform_done