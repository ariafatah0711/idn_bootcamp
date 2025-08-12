"""
Configuration Manager for Security Scanner Application

Handles loading and managing configuration for scanners including
which scanners are active and their settings.
"""

import json
import os
from typing import Dict, Any, Optional

# Try to import yaml, but make it optional
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigManager:
    """
    Manages configuration for the security scanner application.
    
    Supports both JSON and YAML configuration files and provides
    default configurations if no config file is found.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """
        Find configuration file in common locations.
        
        Returns:
            Path to configuration file if found, None otherwise
        """
        # Check current directory first
        current_dir = os.getcwd()
        config_files = [
            os.path.join(current_dir, 'config.json'),
            os.path.join(current_dir, 'config.yaml'),
            os.path.join(current_dir, 'config.yml')
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                return config_file
        
        # Check parent directories
        parent_dir = os.path.dirname(current_dir)
        while parent_dir and parent_dir != os.path.dirname(parent_dir):
            config_files = [
                os.path.join(parent_dir, 'config.json'),
                os.path.join(parent_dir, 'config.yaml'),
                os.path.join(parent_dir, 'config.yml')
            ]
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    return config_file
            
            parent_dir = os.path.dirname(parent_dir)
        
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path:
            return self._get_default_config()
        
        try:
            if self.config_path.endswith('.json'):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            elif self.config_path.endswith(('.yaml', '.yml')):
                if not YAML_AVAILABLE:
                    print(f"Warning: YAML support not available. Install PyYAML to use {self.config_path}")
                    return self._get_default_config()
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            else:
                print(f"Warning: Unsupported config file format: {self.config_path}")
                return self._get_default_config()
            
            # Validate and merge with defaults
            default_config = self._get_default_config()
            return self._merge_configs(default_config, config)
            
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_path}: {str(e)}")
            print("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration for all scanners.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "scanners": {
                "docker_scanner": {
                    "active": True,
                    "description": "Dockerfile security scanner using hadolint and trivy",
                    "extensions": ["Dockerfile", "dockerfile", ".dockerfile"],
                    "tools": {
                        "hadolint": {
                            "command": "hadolint",
                            "args": ["--format", "json"],
                            "required": True
                        },
                        "trivy": {
                            "command": "trivy",
                            "args": ["config", "--format", "json"],
                            "required": False
                        }
                    }
                },
                "k8s_scanner": {
                    "active": True,
                    "description": "Kubernetes manifest security scanner using kube-score",
                    "extensions": [".yaml", ".yml", ".json"],
                    "tools": {
                        "kube_score": {
                            "command": "kube-score",
                            "args": ["--output-format", "json"],
                            "required": True
                        }
                    }
                },
                "terraform_scanner": {
                    "active": True,
                    "description": "Terraform security scanner using tfsec and checkov",
                    "extensions": [".tf", ".tfvars", ".hcl"],
                    "tools": {
                        "tfsec": {
                            "command": "tfsec",
                            "args": ["--format", "json"],
                            "required": False
                        },
                        "checkov": {
                            "command": "checkov",
                            "args": ["-f", "PLACEHOLDER", "--output", "json"],
                            "required": False
                        }
                    }
                }
            },
            "output": {
                "default_format": "json",
                "include_timestamp": True,
                "include_metadata": True
            },
            "logging": {
                "level": "INFO",
                "include_tool_output": True
            }
        }
    
    def _merge_configs(self, default_config: Dict[str, Any], user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge user configuration with defaults.
        
        Args:
            default_config: Default configuration
            user_config: User-provided configuration
            
        Returns:
            Merged configuration
        """
        merged = default_config.copy()
        
        def deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> None:
            """Recursively merge nested dictionaries."""
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        deep_merge(merged, user_config)
        return merged
    
    def get_scanner_config(self, scanner_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific scanner.
        
        Args:
            scanner_name: Name of the scanner
            
        Returns:
            Scanner configuration or None if not found
        """
        return self.config.get("scanners", {}).get(scanner_name)
    
    def is_scanner_active(self, scanner_name: str) -> bool:
        """
        Check if a scanner is active.
        
        Args:
            scanner_name: Name of the scanner
            
        Returns:
            True if scanner is active, False otherwise
        """
        scanner_config = self.get_scanner_config(scanner_name)
        return scanner_config.get("active", False) if scanner_config else False
    
    def get_scanner_extensions(self, scanner_name: str) -> list:
        """
        Get supported file extensions for a scanner.
        
        Args:
            scanner_name: Name of the scanner
            
        Returns:
            List of supported file extensions
        """
        scanner_config = self.get_scanner_config(scanner_name)
        return scanner_config.get("extensions", []) if scanner_config else []
    
    def get_all_scanners(self) -> Dict[str, Dict[str, Any]]:
        """
        Get configuration for all scanners.
        
        Returns:
            Dictionary of all scanner configurations
        """
        return self.config.get("scanners", {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """
        Get output configuration.
        
        Returns:
            Output configuration dictionary
        """
        return self.config.get("output", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Logging configuration dictionary
        """
        return self.config.get("logging", {})
    
    def save_config(self, config_path: Optional[str] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_path: Optional path to save configuration
        """
        save_path = config_path or self.config_path or "config.json"
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            if save_path.endswith('.json'):
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
            elif save_path.endswith(('.yaml', '.yml')):
                if not YAML_AVAILABLE:
                    print(f"Warning: Cannot save YAML file. PyYAML not available. Saving as JSON instead.")
                    save_path = save_path.replace('.yaml', '.json').replace('.yml', '.json')
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config, f, indent=2, ensure_ascii=False)
                else:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            print(f"Configuration saved to: {save_path}")
            
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
    
    def update_scanner_status(self, scanner_name: str, active: bool) -> None:
        """
        Update the active status of a scanner.
        
        Args:
            scanner_name: Name of the scanner
            active: Whether the scanner should be active
        """
        if scanner_name in self.config.get("scanners", {}):
            self.config["scanners"][scanner_name]["active"] = active
            print(f"Scanner '{scanner_name}' {'activated' if active else 'deactivated'}")
        else:
            print(f"Scanner '{scanner_name}' not found in configuration")
