#!/bin/sh

# PDF Extraction Development Server
# This script activates the virtual environment and starts the Streamlit web application

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
else
    echo "No virtual environment found, using system Python"
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt

# Generate data if files don't exist
if [ ! -f "pdfData.json" ] || [ ! -f "data.sqlite" ]; then
    echo "Generating data from PDF..."
    python generateData.py
fi

# Start the Streamlit web application
echo "Starting PDF Extraction Web Application..."
echo "Access the application at: http://localhost:8501"
python -m streamlit run webApp.py 