#!/bin/bash

# Polish Vehicle Registration Certificate QR Code Reader and Decoder
# Setup script for easy installation and configuration

set -e  # Exit on any error

echo "Polish Vehicle Registration Certificate QR Code Reader and Decoder"
echo "=================================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Install system dependencies based on OS
echo ""
echo "Installing system dependencies..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux system"
    if command -v apt-get &> /dev/null; then
        echo "Installing dependencies with apt..."
        sudo apt update
        sudo apt install -y python3-venv python3-pip libzbar0
    elif command -v yum &> /dev/null; then
        echo "Installing dependencies with yum..."
        sudo yum install -y python3-venv python3-pip zbar
    else
        echo "⚠️  Could not detect package manager. Please install:"
        echo "   - python3-venv"
        echo "   - python3-pip" 
        echo "   - libzbar0 (or zbar)"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS system"
    if command -v brew &> /dev/null; then
        echo "Installing dependencies with Homebrew..."
        brew install zbar
    else
        echo "⚠️  Homebrew not found. Please install Homebrew and run:"
        echo "   brew install zbar"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Detected Windows system"
    echo "✓ Windows dependencies are included with Python packages"
else
    echo "⚠️  Unknown operating system: $OSTYPE"
    echo "Please manually install zbar library for your system"
fi

echo ""
echo "Setting up Python virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Created virtual environment"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install packages
echo "Installing Python packages..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo ""
echo "Making scripts executable..."
chmod +x *.py

echo ""
echo "Running tests..."
python test_example.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Usage:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Process a QR code image:"
echo "     python main.py your_image.jpg"
echo ""
echo "  3. Get help:"
echo "     python main.py --help"
echo ""
echo "  4. Run tests:"
echo "     python test_example.py"
echo ""
echo "For more information, see README.md"