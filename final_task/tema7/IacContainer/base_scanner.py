"""
Base Scanner Class for Security Scanner Application

Defines the interface that all security scanners must implement.
This provides a consistent API for different types of security scanning tools.
"""

import json
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from config_manager import ConfigManager


class BaseScanner(ABC):
    """
    Abstract base class for all security scanners.
    
    Defines the interface that must be implemented by specific scanner
    implementations for different file types and security tools.
    """
    
    def __init__(self, config_manager: ConfigManager, scanner_name: str):
        """
        Initialize the base scanner.
        
        Args:
            config_manager: Configuration manager instance
            scanner_name: Name of the scanner (should match config.json keys)
        """
        self.config_manager = config_manager
        self.scanner_name = scanner_name
        self.scanner_config = config_manager.get_scanner_config(self.scanner_name)
    
    @abstractmethod
    def can_scan_file(self, file_path: str, file_name: str, file_ext: str) -> bool:
        """
        Determine if this scanner can handle the given file.
        
        Args:
            file_path: Full path to the file
            file_name: Name of the file
            file_ext: File extension (with dot)
            
        Returns:
            True if this scanner can scan the file, False otherwise
        """
        pass
    
    @abstractmethod
    def scan(self, file_path: str) -> Dict[str, Any]:
        """
        Perform security scan on the specified file.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Dictionary containing scan results
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of what this scanner does.
        
        Returns:
            Description string
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of file extensions this scanner supports.
        
        Returns:
            List of supported file extensions
        """
        pass
    
    @abstractmethod
    def get_required_tools(self) -> List[str]:
        """
        Get list of required CLI tools for this scanner.
        
        Returns:
            List of required tool names
        """
        pass
    
    def test_tools(self) -> Dict[str, bool]:
        """
        Test if required tools are available on the system.
        
        Returns:
            Dictionary mapping tool names to availability status
        """
        results = {}
        
        if not self.scanner_config:
            return results
        
        tools_config = self.scanner_config.get('tools', {})
        
        for tool_name, tool_config in tools_config.items():
            command = tool_config.get('command', tool_name)
            results[tool_name] = self._is_tool_available(command)
        
        return results
    
    def _is_tool_available(self, tool_name: str) -> bool:
        """
        Check if a CLI tool is available on the system.
        
        Args:
            tool_name: Name of the tool to check
            
        Returns:
            True if tool is available, False otherwise
        """
        try:
            # Use 'which' on Unix-like systems, 'where' on Windows
            if sys.platform.startswith('win'):
                result = subprocess.run(['where', tool_name], 
                                      capture_output=True, text=True, check=False)
            else:
                result = subprocess.run(['which', tool_name], 
                                      capture_output=True, text=True, check=False)
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def _run_tool(self, tool_name: str, file_path: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run a security tool and capture its output.
        
        Args:
            tool_name: Name of the tool to run
            file_path: Path to the file being scanned
            args: Optional command line arguments (if not provided, uses config)
            
        Returns:
            Dictionary containing tool execution results
            
        Raises:
            RuntimeError: If tool execution fails
        """
        if not self.scanner_config:
            raise RuntimeError(f"No configuration found for scanner: {self.scanner_name}")
        
        tools_config = self.scanner_config.get('tools', {})
        tool_config = tools_config.get(tool_name)
        
        if not tool_config:
            raise RuntimeError(f"No configuration found for tool: {tool_name}")
        
        command = tool_config.get('command', tool_name)
        
        # Use provided args or fall back to config args
        if args is not None:
            base_args = args
        else:
            base_args = tool_config.get('args', [])
        
        # Replace placeholder with actual file path
        processed_args = []
        for arg in base_args:
            if arg == "PLACEHOLDER":
                processed_args.append(file_path)
            else:
                processed_args.append(arg)
        
        # Check if tool is available
        if not self._is_tool_available(command):
            required = tool_config.get('required', False)
            if required:
                raise RuntimeError(f"Required tool '{command}' is not available")
            else:
                return {
                    "tool": tool_name,
                    "status": "skipped",
                    "reason": f"Tool '{command}' not available"
                }
        
        try:
            # Run the tool
            cmd = [command] + processed_args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=False
            )
            
            # Parse output
            output = {
                "tool": tool_name,
                "command": " ".join(cmd),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": "success" if result.returncode == 0 else "failed"
            }
            
            # Try to parse JSON output if available
            if result.stdout.strip():
                try:
                    output["json_output"] = json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Not JSON, keep as raw text
                    pass
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                "tool": tool_name,
                "status": "timeout",
                "reason": "Tool execution timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "tool": tool_name,
                "status": "error",
                "reason": str(e)
            }
    
    def _get_scan_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get metadata about the file being scanned.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file metadata
        """
        try:
            stat = os.stat(file_path)
            return {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "file_size": stat.st_size,
                "file_type": self._get_file_type(file_path),
                "scanner": self.scanner_name,
                "timestamp": stat.st_mtime
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "error": f"Could not get file metadata: {str(e)}"
            }
    
    def _get_file_type(self, file_path: str) -> str:
        """
        Determine the type of file based on extension and content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            String describing the file type
        """
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Check for specific file types
        if file_name.lower() in ['dockerfile', 'dockerfile.']:
            return "Dockerfile"
        elif file_ext in ['.yaml', '.yml']:
            return "YAML"
        elif file_ext == '.json':
            return "JSON"
        elif file_ext == '.tf':
            return "Terraform"
        elif file_ext == '.tfvars':
            return "Terraform Variables"
        elif file_ext == '.hcl':
            return "HCL"
        else:
            return "Unknown"
    
    def _validate_file_exists(self, file_path: str) -> None:
        """
        Validate that the file exists and is readable.
        
        Args:
            file_path: Path to the file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file is not readable
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"File not readable: {file_path}")
    
    def _get_output_config(self) -> Dict[str, Any]:
        """
        Get output configuration for this scanner.
        
        Returns:
            Output configuration dictionary
        """
        return self.config_manager.get_output_config()
