#!/usr/bin/env python3
"""
GUI Launcher for Code Smell Detector
This script launches the graphical user interface
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from detector_gui import main
    
    if __name__ == "__main__":
        print("🔍 Launching Code Smell Detector GUI...")
        main()
        
except ImportError as e:
    print(f"Error: Failed to import GUI components: {e}")
    print("Make sure all required files are in the src/ directory")
    sys.exit(1)
except Exception as e:
    print(f"Error: Failed to start GUI: {e}")
    sys.exit(1)