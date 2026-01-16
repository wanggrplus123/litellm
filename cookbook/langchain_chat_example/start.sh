#!/bin/bash

# Quick start script for LangChain Chat Application

set -e

echo "=========================================="
echo "LangChain Chat Application - Quick Start"
echo "=========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python is installed: $(python3 --version)"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration:"
    echo "   - Set your DASHSCOPE_API_KEY"
    echo "   - Configure REDIS_URL if needed"
    echo
    echo "Edit .env file now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ .env file exists"
fi
echo

# Check if Redis is running (optional)
echo "🔍 Checking Redis connection..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis is not responding. Make sure Redis is running:"
        echo "   - Install: https://redis.io/docs/install/"
        echo "   - Or use Docker: docker run -d -p 6379:6379 redis:7-alpine"
    fi
else
    echo "⚠️  redis-cli not found. Cannot check Redis status."
    echo "   Make sure Redis is running before starting the application."
fi
echo

echo "=========================================="
echo "🚀 Ready to start the application!"
echo "=========================================="
echo
echo "Run one of the following commands:"
echo "  1. Development mode:  python app/main.py"
echo "  2. With auto-reload:  uvicorn app.main:app --reload"
echo "  3. Production mode:   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4"
echo
echo "After starting, visit:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health:   http://localhost:8000/health"
echo
