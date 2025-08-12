#!/usr/bin/env python3
"""
Simple test script to verify the security scanner application functionality.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported."""
    try:
        from config_manager import ConfigManager
        print("✓ ConfigManager imported successfully")
        
        from base_scanner import BaseScanner
        print("✓ BaseScanner imported successfully")
        
        from scanner_manager import ScannerManager
        print("✓ ScannerManager imported successfully")
        
        from app import SecurityScannerApp
        print("✓ SecurityScannerApp imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config_manager():
    """Test configuration manager functionality."""
    try:
        from config_manager import ConfigManager
        
        config = ConfigManager()
        scanners = config.get_all_scanners()
        
        print(f"✓ ConfigManager created successfully")
        print(f"✓ Found {len(scanners)} scanners in configuration")
        
        return True
    except Exception as e:
        print(f"✗ ConfigManager error: {e}")
        return False

def test_scanner_manager():
    """Test scanner manager functionality."""
    try:
        from config_manager import ConfigManager
        from scanner_manager import ScannerManager
        
        config = ConfigManager()
        scanner_manager = ScannerManager(config)
        
        print(f"✓ ScannerManager created successfully")
        print(f"✓ Loaded {len(scanner_manager.scanners)} scanners")
        
        return True
    except Exception as e:
        print(f"✗ ScannerManager error: {e}")
        return False

def test_app_creation():
    """Test main application creation."""
    try:
        from app import SecurityScannerApp
        
        app = SecurityScannerApp()
        print("✓ SecurityScannerApp created successfully")
        
        return True
    except Exception as e:
        print(f"✗ SecurityScannerApp error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Security Scanner Application...")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Config Manager", test_config_manager),
        ("Scanner Manager", test_scanner_manager),
        ("Application Creation", test_app_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
