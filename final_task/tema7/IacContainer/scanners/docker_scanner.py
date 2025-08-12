"""
Docker Security Scanner

Scans Dockerfiles for security issues using hadolint and trivy.
"""

import os
from typing import Dict, Any, List

from base_scanner import BaseScanner


class DockerScanner(BaseScanner):
    """Security scanner for Dockerfiles and Docker-related files."""
    
    def __init__(self, config_manager, scanner_name: str):
        """Initialize Docker scanner."""
        super().__init__(config_manager, scanner_name)
    
    def can_scan_file(self, file_path: str, file_name: str, file_ext: str) -> bool:
        """Check if this scanner can handle the given file."""
        # Check for Dockerfile (case insensitive)
        if file_name.lower() in ['dockerfile', 'dockerfile.']:
            return True
        
        # Check for .dockerfile extension
        if file_ext == '.dockerfile':
            return True
        
        # Check if file contains Docker-related content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1024).lower()
                if any(keyword in content for keyword in ['from ', 'run ', 'cmd ', 'entrypoint ']):
                    return True
        except Exception:
            pass
        
        return False
    
    def scan(self, file_path: str) -> Dict[str, Any]:
        """Perform security scan on Dockerfile."""
        self._validate_file_exists(file_path)
        metadata = self._get_scan_metadata(file_path)
        
        scan_results = {
            "metadata": metadata,
            "scanner": "docker_scanner",
            "tools": {}
        }
        
        # Run hadolint
        try:
            hadolint_result = self._run_tool("hadolint", file_path)
            scan_results["tools"]["hadolint"] = hadolint_result
        except Exception as e:
            scan_results["tools"]["hadolint"] = {
                "tool": "hadolint",
                "status": "error",
                "reason": str(e)
            }
        
        # Run trivy
        try:
            trivy_result = self._run_tool("trivy", file_path)
            scan_results["tools"]["trivy"] = trivy_result
        except Exception as e:
            scan_results["tools"]["trivy"] = {
                "tool": "trivy",
                "status": "error",
                "reason": str(e)
            }
        
        scan_results["overall_status"] = self._determine_overall_status(scan_results["tools"])
        return scan_results
    
    def get_description(self) -> str:
        """Get description of this scanner."""
        return "Dockerfile security scanner using hadolint and trivy"
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return ["Dockerfile", "dockerfile", ".dockerfile"]
    
    def _determine_overall_status(self, tools_results: Dict[str, Any]) -> str:
        """Determine overall scan status based on tool results."""
        if not tools_results:
            return "no_tools_available"
        
        failed_tools = [
            tool for tool, result in tools_results.items()
            if result.get("status") == "failed"
        ]
        
        if failed_tools:
            return "partial_failure"
        
        successful_tools = [
            tool for tool, result in tools_results.items()
            if result.get("status") == "success"
        ]
        
        if successful_tools:
            return "success"
        
        return "no_tools_available"
