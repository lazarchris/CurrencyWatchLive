#!/bin/bash

# Check if venv exists and delete it if it does
if [ -d "venv" ]; then
    echo "Deleting existing venv..."
    rm -rf venv
fi

# Create and activate a new virtual environment
echo "Creating new venv..."
python3 -m venv venv
source venv/bin/activate

# Run Python script
echo "Running Python app..."
python3 ./app/main.py 
echo "Data streaming is in progress..."

# Deactivate virtual environment
deactivate
