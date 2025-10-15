#!/bin/bash
# DL_Assistant One-Click Installer for Linux/Unix/MacOS
# This script installs DL_Assistant and launches the configuration dashboard

set -e

echo "======================================"
echo "DL_Assistant One-Click Installer"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3.8+ is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
echo ""

# Check if pip is installed
echo "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed.${NC}"
    echo "Please install pip3 to continue."
    exit 1
fi

echo -e "${GREEN}✓ pip3 detected${NC}"
echo ""

# Install the package
echo "Installing DL_Assistant..."
pip3 install -e . --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ DL_Assistant installed successfully!${NC}"
else
    echo -e "${RED}Error: Installation failed.${NC}"
    exit 1
fi

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo -e "${YELLOW}Opening the configuration dashboard...${NC}"
echo ""
echo "The dashboard will open in your browser at http://127.0.0.1:5000"
echo "You can:"
echo "  - Configure folder paths"
echo "  - Set up naming patterns"
echo "  - Manage file type classifications"
echo "  - Configure duplicate detection"
echo ""
echo -e "${YELLOW}After configuring your preferences:${NC}"
echo "  - Close the dashboard (Ctrl+C in terminal)"
echo "  - Run 'dl-assistant' to start monitoring your downloads folder"
echo "  - Or run 'dl-assistant --mode dashboard' to open dashboard again"
echo ""
echo "Press Ctrl+C to exit the dashboard when you're done configuring."
echo ""
sleep 2

# Try to open browser (cross-platform)
if command -v xdg-open &> /dev/null; then
    # Linux
    (sleep 3 && xdg-open http://127.0.0.1:5000) &
elif command -v open &> /dev/null; then
    # macOS
    (sleep 3 && open http://127.0.0.1:5000) &
fi

# Start the dashboard
dl-assistant --mode dashboard
