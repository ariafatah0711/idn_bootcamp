#!/usr/bin/env python3
"""
Test script to verify the scanner configuration fixes.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scanner_config():
    """Test if scanners can now find their configuration."""
    try:
        from config_manager import ConfigManager
        from scanner_manager import ScannerManager
        
        print("Testing scanner configuration fix...")
        
        # Create config manager
        config = ConfigManager()
        print(f"✓ ConfigManager created")
        
        # Check scanner configurations
        scanners = config.get_all_scanners()
        print(f"✓ Found {len(scanners)} scanners in config:")
        for name in scanners.keys():
            print(f"  - {name}")
        
        # Create scanner manager
        scanner_manager = ScannerManager(config)
        print(f"✓ ScannerManager created")
        
        # Check if scanners loaded correctly
        print(f"✓ Loaded {len(scanner_manager.scanners)} scanners:")
        for name, scanner in scanner_manager.scanners.items():
            print(f"  - {name}: {scanner.__class__.__name__}")
            print(f"    Scanner name: {scanner.scanner_name}")
            print(f"    Has config: {scanner.scanner_config is not None}")
            
            if scanner.scanner_config:
                print(f"    Active: {scanner.scanner_config.get('active', False)}")
                print(f"    Tools: {list(scanner.scanner_config.get('tools', {}).keys())}")
            else:
                print(f"    ⚠️ No configuration found!")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test."""
    print("🔧 Testing Scanner Configuration Fixes")
    print("=" * 50)
    
    if test_scanner_config():
        print("\n🎉 All tests passed! Configuration mismatch should be fixed.")
        print("\nYou can now test with:")
        print("  python3 app.py scan -f examples/Dockerfile")
        print("  python3 app.py scan -f examples/ -o scan-results/")
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
