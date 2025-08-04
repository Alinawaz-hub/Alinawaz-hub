#!/bin/bash

# Polish Vehicle QR Decoder Startup Script

echo "🚗 Starting Polish Vehicle QR Decoder..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Node.js dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Install Python dependencies if needed
echo "🐍 Checking Python dependencies..."
pip3 install -r requirements.txt

# Start Node.js bridge server in background
echo "🔧 Starting Node.js bridge server..."
node node_bridge.js &
NODE_PID=$!

# Wait a moment for Node.js server to start
sleep 3

# Check if Node.js server is running
if curl -s http://localhost:3001/health > /dev/null; then
    echo "✅ Node.js bridge server is running on port 3001"
else
    echo "❌ Failed to start Node.js bridge server"
    kill $NODE_PID 2>/dev/null
    exit 1
fi

# Start Python web server
echo "🌐 Starting Python web server..."
echo "📱 Web interface will be available at: http://localhost:5000"
echo "🔧 API endpoints available at: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $NODE_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start Python web server
python3 web_decoder.py