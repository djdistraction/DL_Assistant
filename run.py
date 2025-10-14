#!/usr/bin/env python3
"""
Quick start script for DL_Assistant
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dl_assistant.main import main

if __name__ == '__main__':
    main()
