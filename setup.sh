#!/bin/bash
# Quick setup script for Raspberry Pi 5 - Optimized for ARM64

echo "======================================"
echo "Heart Sound Classifier - Setup"
echo "======================================"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y python3-pip python3-tk

# Install pre-compiled packages from apt (MUCH faster on RPi)
echo "⚡ Installing pre-compiled packages (faster)..."
sudo apt-get install -y python3-numpy python3-scipy python3-sklearn

# Install remaining packages via pip
echo "🐍 Installing PyWavelets..."
pip3 install PyWavelets

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Testing installation..."
python3 test_system.py

echo ""
echo "To run the application:"
echo "  python3 heart_sound_classifier.py"
echo ""
