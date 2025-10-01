#!/usr/bin/env python3
"""
GUI Test Script - Verify GUI components work correctly
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_gui_components():
    """Test GUI components without launching the full interface"""
    print("🧪 Testing GUI Components...")
    
    try:
        # Test imports
        print("1. Testing imports...")
        import tkinter as tk
        from detector_engine import CodeSmellDetector
        import yaml
        print("   ✓ All imports successful")
        
        # Test detector initialization
        print("2. Testing detector initialization...")
        detector = CodeSmellDetector()
        available_detectors = detector.get_available_detectors()
        print(f"   ✓ Detector initialized with {len(available_detectors)} detectors")
        print(f"   Available: {', '.join(available_detectors)}")
        
        # Test configuration loading
        print("3. Testing configuration...")
        config = detector.config
        if 'code_smells' in config:
            print("   ✓ Configuration loaded successfully")
            enabled_smells = [name for name, cfg in config['code_smells'].items() if cfg.get('enabled', True)]
            print(f"   Enabled smells: {', '.join(enabled_smells)}")
        else:
            print("   ⚠ Configuration missing code_smells section")
            
        # Test GUI components (without showing window)
        print("4. Testing GUI components...")
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test basic widgets
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Test")
        button = tk.Button(frame, text="Test")
        listbox = tk.Listbox(frame)
        
        print("   ✓ Basic GUI components working")
        
        # Test file operations
        print("5. Testing file operations...")
        test_files = list(Path("test-files").glob("*.java")) if Path("test-files").exists() else []
        print(f"   Found {len(test_files)} test files")
        
        if test_files:
            # Test analysis on first file
            test_file = test_files[0]
            smells = detector.analyze_file(str(test_file))
            print(f"   ✓ Analysis test: {len(smells)} smells found in {test_file.name}")
        
        root.destroy()
        
        print("\n🎉 All tests passed! GUI should work correctly.")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Make sure all required packages are installed:")
        print("   - tkinter (usually included with Python)")
        print("   - PyYAML (pip install PyYAML)")
        return False
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking Requirements...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("   ⚠ Python 3.7+ recommended")
    else:
        print("   ✓ Python version OK")
    
    # Check required packages
    required_packages = ['tkinter', 'yaml', 'pathlib', 'threading']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'yaml':
                import yaml
            elif package == 'pathlib':
                import pathlib
            elif package == 'threading':
                import threading
            print(f"   ✓ {package} available")
        except ImportError:
            print(f"   ❌ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        if 'yaml' in missing_packages:
            print("Install with: pip install PyYAML")
        return False
    else:
        print("   ✓ All required packages available")
        return True

def main():
    """Main test function"""
    print("=" * 60)
    print("🔍 CODE SMELL DETECTOR GUI - TEST SUITE")
    print("=" * 60)
    
    # Check requirements
    requirements_ok = check_requirements()
    print()
    
    if not requirements_ok:
        print("❌ Requirements check failed. Please install missing packages.")
        return 1
    
    # Test components
    components_ok = test_gui_components()
    print()
    
    if components_ok:
        print("✅ All tests passed! You can now run the GUI:")
        print("   python launch_gui.py")
        print("   or")
        print("   run_gui.bat")
        return 0
    else:
        print("❌ Component tests failed. Check error messages above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)