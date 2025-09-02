#!/bin/bash

# Start the Web-Based Report Generator

set -e

echo "🚀 Starting Marketing Report Generator Web App..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Start the Flask app
echo "🌐 Starting web server..."
echo ""
echo "✨ Report Generator is starting up!"
echo "📱 Open your browser to: http://localhost:5000"
echo "📋 Upload any markdown audit file to generate professional reports"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py