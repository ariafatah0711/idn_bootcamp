"""
Scanner Manager for Security Scanner Application

Manages the loading and execution of different security scanners
based on file types and configuration.
"""

import importlib
import os
from typing import Dict, List, Optional, Type, Any

from .base_scanner import BaseScanner
from .config_manager import ConfigManager


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
        try:
            # Import scanner modules directly
            from .scanners.docker_scanner import DockerScanner
            from .scanners.k8s_scanner import K8sScanner
            from .scanners.terraform_scanner import TerraformScanner
            
            # Define scanner classes
            scanner_classes = {
                'docker_scanner': DockerScanner,
                'k8s_scanner': K8sScanner,
                'terraform_scanner': TerraformScanner
            }
            
            # Load active scanners
            for scanner_name, scanner_class in scanner_classes.items():
                if self.config_manager.is_scanner_active(scanner_name):
                    try:
                        scanner_instance = scanner_class(self.config_manager, scanner_name)
                        self.scanners[scanner_name] = scanner_instance
                        print(f"Loaded scanner: {scanner_name}")
                    except Exception as e:
                        print(f"Warning: Error loading scanner {scanner_name}: {str(e)}")
                        
        except ImportError as e:
            print(f"Warning: Could not import scanner modules: {str(e)}")
        except Exception as e:
            print(f"Warning: Error during scanner loading: {str(e)}")
    
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
    
    def get_all_scanners(self) -> Dict[str, Dict[str, Any]]:
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
                'tools': list(scanner.scanner_config.get('tools', {}).keys()) if scanner.scanner_config else []
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
