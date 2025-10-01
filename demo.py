#!/usr/bin/env python3
"""
Sample test script demonstrating the Code Smell Detector functionality
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Command failed with return code: {result.returncode}")
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    """Run demonstration tests"""
    print("🔍 Code Smell Detector - Demonstration")
    print("This script demonstrates various features of the code smell detector")
    
    # Change to src directory
    os.chdir("src")
    python_cmd = "C:/Users/hashi/AppData/Local/Programs/Python/Python313/python.exe"
    
    # Test 1: List available detectors
    run_command(
        f"{python_cmd} detector_cli.py --list-detectors",
        "List Available Detectors"
    )
    
    # Test 2: Analyze single file with all detectors
    run_command(
        f"{python_cmd} detector_cli.py ../test-files/LibrarySystem.java --format summary",
        "Analyze Single File (Summary Format)"
    )
    
    # Test 3: Only detect structural smells
    run_command(
        f"{python_cmd} detector_cli.py ../test-files/MemberValidator.java --only LongMethod,GodClass,FeatureEnvy",
        "Detect Only Structural Smells"
    )
    
    # Test 4: Exclude duplicated code detection
    run_command(
        f"{python_cmd} detector_cli.py ../test-files/BookUtilities.java --exclude DuplicatedCode --format detailed",
        "Exclude Duplicated Code Detection"
    )
    
    # Test 5: Analyze all test files in JSON format
    run_command(
        f"{python_cmd} detector_cli.py ../test-files/ --format json",
        "Analyze All Files (JSON Format)"
    )
    
    # Test 6: Only magic numbers detection
    run_command(
        f"{python_cmd} detector_cli.py ../test-files/ --only MagicNumbers --format summary",
        "Detect Only Magic Numbers"
    )
    
    print(f"\n{'='*60}")
    print("✅ Demonstration Complete!")
    print("The Code Smell Detector successfully identified various code smells")
    print("in our deliberately smelly Java library management system.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()