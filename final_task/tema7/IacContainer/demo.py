#!/usr/bin/env python3
"""
Demonstration script for the Security Scanner Application.
This script shows the core functionality without CLI argument parsing.
"""

import json
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Demonstrate the security scanner functionality."""
    print("🔒 Security File Scanner - Demonstration")
    print("=" * 50)
    
    try:
        # Import the application
        from app import SecurityScannerApp
        
        # Create the application
        app = SecurityScannerApp()
        print("✓ Application created successfully")
        
        # List available scanners
        print("\n📋 Available Scanners:")
        print("-" * 30)
        app.list_scanners()
        
        # Test scanning examples
        examples_dir = "examples"
        if os.path.exists(examples_dir):
            print(f"\n🔍 Testing Scanner with Examples:")
            print("-" * 30)
            
            # Test individual files
            test_files = [
                "examples/Dockerfile",
                "examples/deployment.yaml", 
                "examples/main.tf"
            ]
            
            for test_file in test_files:
                if os.path.exists(test_file):
                    print(f"\n📁 Testing: {test_file}")
                    try:
                        # Get scanner for this file
                        scanner = app.scanner_manager.get_scanner_for_file(test_file)
                        if scanner:
                            print(f"  ✓ Found scanner: {scanner.__class__.__name__}")
                            
                            # Test tool availability
                            tools_status = scanner.test_tools()
                            print(f"  🔧 Tools status:")
                            for tool, available in tools_status.items():
                                status = "✓ Available" if available else "✗ Not Available"
                                print(f"    {tool}: {status}")
                        else:
                            print(f"  ✗ No suitable scanner found")
                    except Exception as e:
                        print(f"  ✗ Error: {str(e)}")
                else:
                    print(f"  ⚠️ File not found: {test_file}")
            
            # Test directory scanning
            print(f"\n📂 Testing Directory Scan:")
            print("-" * 30)
            try:
                app.run_scan(examples_dir)
                print("✓ Directory scan completed")
            except Exception as e:
                print(f"✗ Directory scan error: {str(e)}")
        
        else:
            print(f"\n⚠️ Examples directory not found: {examples_dir}")
            print("Please create the examples directory with test files first.")
        
        print("\n🎉 Demonstration completed successfully!")
        print("\nTo use the full CLI functionality:")
        print("  python3 app.py list")
        print("  python3 app.py scan -f examples/Dockerfile")
        print("  python3 app.py scan -f examples/ -o scan-results/")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please ensure all required modules are available.")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
