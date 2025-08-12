"""
Scanner Manager for Security Scanner Application

Manages the loading and execution of different security scanners
based on file types and configuration.
"""

import importlib
import os
from typing import Dict, List, Optional, Type

from base_scanner import BaseScanner
from config_manager import ConfigManager


class ScannerManager:
    """
    Manages all available security scanners.
    
    Loads scanner modules dynamically, determines which scanner to use
    for each file type, and provides access to scanner information.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the scanner manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.scanners: Dict[str, BaseScanner] = {}
        self._load_scanners()
    
    def _load_scanners(self) -> None:
        """Load all available scanner modules."""
        scanners_dir = "scanners"
        
        if not os.path.exists(scanners_dir):
            print(f"Warning: Scanners directory '{scanners_dir}' not found")
            return
        
        # Get list of Python files in scanners directory
        scanner_files = [
            f for f in os.listdir(scanners_dir)
            if f.endswith('.py') and not f.startswith('__')
        ]
        
        for scanner_file in scanner_files:
            scanner_name = scanner_file[:-3]  # Remove .py extension
            
            # Check if scanner is active in configuration
            if not self.config_manager.is_scanner_active(scanner_name):
                continue
            
            try:
                # Import scanner module
                module_name = f"scanners.{scanner_name}"
                module = importlib.import_module(module_name)
                
                # Look for scanner class (convention: class name should match file name in CamelCase)
                class_name = self._to_camel_case(scanner_name)
                scanner_class = getattr(module, class_name, None)
                
                if scanner_class and issubclass(scanner_class, BaseScanner):
                    # Initialize scanner instance with the correct scanner name
                    scanner_instance = scanner_class(self.config_manager, scanner_name)
                    self.scanners[scanner_name] = scanner_instance
                    print(f"Loaded scanner: {scanner_name}")
                else:
                    print(f"Warning: No valid scanner class found in {scanner_file}")
                    
            except ImportError as e:
                print(f"Warning: Could not import scanner {scanner_name}: {str(e)}")
            except Exception as e:
                print(f"Warning: Error loading scanner {scanner_name}: {str(e)}")
    
    def _to_camel_case(self, snake_case: str) -> str:
        """
        Convert snake_case to CamelCase.
        
        Args:
            snake_case: String in snake_case format
            
        Returns:
            String in CamelCase format
        """
        return ''.join(word.capitalize() for word in snake_case.split('_'))
    
    def get_scanner_for_file(self, file_path: str) -> Optional[BaseScanner]:
        """
        Get the appropriate scanner for a given file.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Scanner instance if found, None otherwise
        """
        if not os.path.exists(file_path):
            return None
        
        # Get file extension and name
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Check each scanner to see if it can handle this file
        for scanner_name, scanner in self.scanners.items():
            if scanner.can_scan_file(file_path, file_name, file_ext):
                return scanner
        
        return None
    
    def get_all_scanners(self) -> Dict[str, Dict[str, any]]:
        """
        Get information about all available scanners.
        
        Returns:
            Dictionary containing scanner information
        """
        scanner_info = {}
        
        for scanner_name, scanner in self.scanners.items():
            scanner_info[scanner_name] = {
                'active': True,
                'description': scanner.get_description(),
                'extensions': scanner.get_supported_extensions(),
                'tools': scanner.get_required_tools()
            }
        
        # Add inactive scanners from configuration
        config_scanners = self.config_manager.get_all_scanners()
        for scanner_name, config in config_scanners.items():
            if scanner_name not in scanner_info:
                scanner_info[scanner_name] = {
                    'active': config.get('active', False),
                    'description': config.get('description', 'No description available'),
                    'extensions': config.get('extensions', []),
                    'tools': list(config.get('tools', {}).keys())
                }
        
        return scanner_info
    
    def get_scanner(self, scanner_name: str) -> Optional[BaseScanner]:
        """
        Get a specific scanner by name.
        
        Args:
            scanner_name: Name of the scanner
            
        Returns:
            Scanner instance if found, None otherwise
        """
        return self.scanners.get(scanner_name)
    
    def reload_scanners(self) -> None:
        """Reload all scanner modules."""
        print("Reloading scanners...")
        self.scanners.clear()
        self._load_scanners()
    
    def test_scanner_tools(self) -> Dict[str, Dict[str, bool]]:
        """
        Test if required tools for each scanner are available.
        
        Returns:
            Dictionary mapping scanner names to tool availability status
        """
        results = {}
        
        for scanner_name, scanner in self.scanners.items():
            results[scanner_name] = scanner.test_tools()
        
        return results
    
    def get_supported_file_types(self) -> List[str]:
        """
        Get all supported file extensions across all scanners.
        
        Returns:
            List of supported file extensions
        """
        extensions = set()
        
        for scanner in self.scanners.values():
            extensions.update(scanner.get_supported_extensions())
        
        return sorted(list(extensions))
    
    def scan_file_with_scanner(self, file_path: str, scanner_name: str) -> Optional[Dict]:
        """
        Scan a file using a specific scanner.
        
        Args:
            file_path: Path to the file to scan
            scanner_name: Name of the scanner to use
            
        Returns:
            Scan results if successful, None otherwise
        """
        scanner = self.get_scanner(scanner_name)
        if not scanner:
            print(f"Scanner '{scanner_name}' not found")
            return None
        
        if not scanner.can_scan_file(file_path, os.path.basename(file_path), os.path.splitext(file_path)[1].lower()):
            print(f"Scanner '{scanner_name}' cannot scan file '{file_path}'")
            return None
        
        try:
            return scanner.scan(file_path)
        except Exception as e:
            print(f"Error scanning {file_path} with {scanner_name}: {str(e)}")
            return None
