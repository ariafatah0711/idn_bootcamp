#!/usr/bin/env python3
"""
Security File Scanner - Modular Security Scanning Automation Tool

Usage:
    python3 app.py scan -f /path/to/dir
    python3 app.py scan -f /path/to/file -o output.json
    python3 app.py scan -f /path/to/file -o /output/dir/
    python3 app.py list
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional

from utils.scanner_manager import ScannerManager
from utils.config_manager import ConfigManager


class SecurityScannerApp:
    """Main application class for security scanning automation."""
    
    def __init__(self):
        """Initialize the application with configuration and scanner manager."""
        self.config_manager = ConfigManager()
        self.scanner_manager = ScannerManager(self.config_manager)
    
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments using argparse."""
        parser = argparse.ArgumentParser(
            description="Modular Security File Scanner",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python3 app.py scan -f /path/to/directory
  python3 app.py scan -f /path/to/file -o output.json
  python3 app.py scan -f /path/to/file -o /output/dir/
  python3 app.py list
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Scan command
        scan_parser = subparsers.add_parser('scan', help='Run security scan on files/directories')
        scan_parser.add_argument(
            '-f', '--file',
            required=True,
            help='File or directory path to scan'
        )
        scan_parser.add_argument(
            '-o', '--output',
            help='Output file path or directory for scan results'
        )
        
        # List command
        subparsers.add_parser('list', help='Show available scanners and their status')
        
        return parser.parse_args()
    
    def run_scan(self, file_path: str, output_path: Optional[str] = None) -> None:
        """Execute security scan on the specified file or directory."""
        try:
            if not os.path.exists(file_path):
                print(f"Error: Path '{file_path}' does not exist")
                sys.exit(1)
            
            if os.path.isfile(file_path):
                self._scan_single_file(file_path, output_path)
            elif os.path.isdir(file_path):
                self._scan_directory(file_path, output_path)
            else:
                print(f"Error: '{file_path}' is neither a file nor directory")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error during scan: {str(e)}")
            sys.exit(1)
    
    def _scan_single_file(self, file_path: str, output_path: Optional[str] = None) -> None:
        """Scan a single file using appropriate scanner."""
        print(f"Scanning file: {file_path}")
        
        scanner = self.scanner_manager.get_scanner_for_file(file_path)
        if not scanner:
            print(f"No suitable scanner found for file: {file_path}")
            return
        
        try:
            scan_result = scanner.scan(file_path)
            
            if output_path:
                self._save_scan_result(scan_result, output_path, file_path)
            else:
                print(json.dumps(scan_result, indent=2))
                
        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
    
    def _scan_directory(self, dir_path: str, output_path: Optional[str] = None) -> None:
        """Scan all supported files in a directory."""
        print(f"Scanning directory: {dir_path}")
        
        supported_files = self._find_supported_files(dir_path)
        
        if not supported_files:
            print(f"No supported files found in directory: {dir_path}")
            return
        
        print(f"Found {len(supported_files)} supported files to scan")
        
        all_results = {}
        for file_path in supported_files:
            try:
                scanner = self.scanner_manager.get_scanner_for_file(file_path)
                if scanner:
                    print(f"Scanning: {file_path}")
                    scan_result = scanner.scan(file_path)
                    all_results[file_path] = scan_result
            except Exception as e:
                print(f"Error scanning {file_path}: {str(e)}")
                all_results[file_path] = {"error": str(e)}
        
        if output_path:
            self._save_scan_result(all_results, output_path, dir_path)
        else:
            print(json.dumps(all_results, indent=2))
    
    def _find_supported_files(self, dir_path: str) -> List[str]:
        """Find all supported files in a directory."""
        supported_files = []
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.scanner_manager.get_scanner_for_file(file_path):
                    supported_files.append(file_path)
        
        return supported_files
    
    def _save_scan_result(self, scan_result: Dict, output_path: str, source_path: str) -> None:
        """Save scan results to the specified output path."""
        try:
            if os.path.isdir(output_path):
                source_name = os.path.basename(source_path)
                if os.path.isdir(source_path):
                    filename = f"{source_name}_scan_results.json"
                else:
                    filename = f"{os.path.splitext(source_name)[0]}_scan_results.json"
                output_file = os.path.join(output_path, filename)
            else:
                output_file = output_path
            
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scan_result, f, indent=2, ensure_ascii=False)
            
            print(f"Scan results saved to: {output_file}")
            
        except Exception as e:
            print(f"Error saving scan results: {str(e)}")
    
    def list_scanners(self) -> None:
        """Display available scanners and their status."""
        print("Available Security Scanners:")
        print("=" * 50)
        
        scanners = self.scanner_manager.get_all_scanners()
        
        for scanner_name, scanner_info in scanners.items():
            status = "✓ Active" if scanner_info['active'] else "✗ Inactive"
            description = scanner_info.get('description', 'No description available')
            print(f"\n{scanner_name}:")
            print(f"  Status: {status}")
            print(f"  Description: {description}")
            print(f"  Supported Extensions: {', '.join(scanner_info.get('extensions', []))}")
    
    def run(self) -> None:
        """Main application entry point."""
        try:
            args = self.parse_arguments()
            
            if args.command == 'scan':
                self.run_scan(args.file, args.output)
            elif args.command == 'list':
                self.list_scanners()
            else:
                print("Please specify a command. Use -h for help.")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\nScan interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            sys.exit(1)


def main():
    """Main function to run the security scanner application."""
    app = SecurityScannerApp()
    app.run()


if __name__ == "__main__":
    main()