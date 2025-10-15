#!/bin/bash
# DL_Assistant Dashboard Launcher
# Quick launcher to open the configuration dashboard

echo "Opening DL_Assistant Dashboard..."
echo "Dashboard will be available at http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to close the dashboard."
echo ""

# Try to open browser (cross-platform)
if command -v xdg-open &> /dev/null; then
    # Linux
    (sleep 2 && xdg-open http://127.0.0.1:5000) &
elif command -v open &> /dev/null; then
    # macOS
    (sleep 2 && open http://127.0.0.1:5000) &
fi

# Start the dashboard
dl-assistant --mode dashboard
