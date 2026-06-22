#!/bin/bash

# Start MCP Client Demo

echo "🚀 Starting MCP Client Demo..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Please run start-server.sh first"
    exit 1
fi

source venv/bin/activate

# Check if server is running
if ! curl -s http://localhost:8000/sse > /dev/null; then
    echo "⚠️  Server is not running. Please start the server first with ./start-server.sh"
    exit 1
fi

# Start client demo
cd client
echo "✅ Running client demo..."
python client.py
