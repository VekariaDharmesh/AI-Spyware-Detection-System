#!/bin/bash

# Universal Device Manager Startup Script
# Updated from spyware detection to universal device management

echo "🌐 Starting Universal Device Manager..."
echo "=================================="

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Install universal requirements
echo "📦 Installing dependencies..."
pip3 install -r requirements_universal.txt

# Get local IP for network access
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    # Try macOS specific command
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null)
fi
if [ -z "$LOCAL_IP" ]; then
    # Fallback to localhost
    LOCAL_IP="localhost"
fi

echo "🌐 Network access: http://$LOCAL_IP:8501"
echo "🔗 Local access: http://localhost:8501"
echo ""
echo "📱 Mobile users: Connect to the same Wi-Fi and open:"
echo "   http://$LOCAL_IP:8501"
echo ""
echo "Starting Streamlit server..."
echo "=================================="

# Start the universal app
streamlit run universal_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true