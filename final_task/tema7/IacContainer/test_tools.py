#!/usr/bin/env python3
"""
Test script to verify tool command fixes.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_docker_scanner():
    """Test Docker scanner with fixed tool commands."""
    try:
        from config_manager import ConfigManager
        from scanner_manager import ScannerManager
        
        print("Testing Docker scanner tool commands...")
        
        # Create managers
        config = ConfigManager()
        scanner_manager = ScannerManager(config)
        
        # Get Docker scanner
        docker_scanner = scanner_manager.scanners.get('docker_scanner')
        if not docker_scanner:
            print("✗ Docker scanner not found")
            return False
        
        print(f"✓ Docker scanner: {docker_scanner.__class__.__name__}")
        print(f"  Scanner name: {docker_scanner.scanner_name}")
        print(f"  Has config: {docker_scanner.scanner_config is not None}")
        
        if docker_scanner.scanner_config:
            tools = docker_scanner.scanner_config.get('tools', {})
            print(f"  Tools configured: {list(tools.keys())}")
            
            for tool_name, tool_config in tools.items():
                command = tool_config.get('command', tool_name)
                args = tool_config.get('args', [])
                print(f"    {tool_name}: {command} {' '.join(args)}")
        
        # Test tool execution (this will fail if tools aren't installed, but should show correct commands)
        test_file = "examples/Dockerfile"
        if os.path.exists(test_file):
            print(f"\nTesting scan with {test_file}...")
            try:
                result = docker_scanner.scan(test_file)
                print("✓ Scan completed")
                print(f"  Overall status: {result.get('overall_status')}")
                
                tools_result = result.get('tools', {})
                for tool_name, tool_result in tools_result.items():
                    status = tool_result.get('status', 'unknown')
                    command = tool_result.get('command', 'unknown')
                    print(f"    {tool_name}: {status} - {command}")
                    
            except Exception as e:
                print(f"✗ Scan failed: {e}")
                return False
        else:
            print(f"⚠️ Test file not found: {test_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test."""
    print("🔧 Testing Tool Command Fixes")
    print("=" * 50)
    
    if test_docker_scanner():
        print("\n🎉 Tool command test passed!")
        print("\nYou can now test with:")
        print("  python3 app.py scan -f examples/Dockerfile")
        print("  python3 app.py scan -f examples/deployment.yaml")
        print("  python3 app.py scan -f examples/main.tf")
    else:
        print("\n❌ Tool command test failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
