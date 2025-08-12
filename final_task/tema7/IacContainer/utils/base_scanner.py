"""
Base Scanner Class for Security Scanner Application

Defines the interface that all security scanners must implement.
"""

import json
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from .config_manager import ConfigManager


class BaseScanner(ABC):
    """Abstract base class for all security scanners."""
    
    def __init__(self, config_manager: ConfigManager, scanner_name: str):
        """Initialize the base scanner."""
        self.config_manager = config_manager
        self.scanner_name = scanner_name
        self.scanner_config = config_manager.get_scanner_config(scanner_name)
    
    @abstractmethod
    def can_scan_file(self, file_path: str, file_name: str, file_ext: str) -> bool:
        """Determine if this scanner can handle the given file."""
        pass
    
    @abstractmethod
    def scan(self, file_path: str) -> Dict[str, Any]:
        """Perform security scan on the specified file."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of what this scanner does."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Get list of file extensions this scanner supports."""
        pass
    
    def _run_tool(self, tool_name: str, file_path: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run a security tool and capture its output."""
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
        
        # Replace placeholders with actual paths
        processed_args = []
        for arg in base_args:
            if arg == "PLACEHOLDER":
                processed_args.append(file_path)
            elif arg == "PLACEHOLDER_DIR":
                file_dir = os.path.dirname(file_path)
                processed_args.append(file_dir if file_dir else ".")
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
                timeout=300,
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
        """Get metadata about the file being scanned."""
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
        """Determine the type of file based on extension and content."""
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
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
        """Validate that the file exists and is readable."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"File not readable: {file_path}")
    
    def _is_tool_available(self, tool_name: str) -> bool:
        """Check if a CLI tool is available on the system."""
        try:
            if sys.platform.startswith('win'):
                result = subprocess.run(['where', tool_name], 
                                      capture_output=True, text=True, check=False)
            else:
                result = subprocess.run(['which', tool_name], 
                                      capture_output=True, text=True, check=False)
            
            return result.returncode == 0
            
        except Exception:
            return False
