"""
Terraform Security Scanner

Scans Terraform files for security issues using tfsec.
"""

import os
import re
from typing import Dict, List, Any

from base_scanner import BaseScanner


class TerraformScanner(BaseScanner):
    """Security scanner for Terraform files."""
    
    def __init__(self, config_manager, scanner_name: str):
        """Initialize Terraform scanner."""
        super().__init__(config_manager, scanner_name)
    
    def can_scan_file(self, file_path: str, file_name: str, file_ext: str) -> bool:
        """Check if this scanner can handle the given file."""
        if file_ext in ['.tf', '.tfvars', '.hcl']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2048).lower()
                    
                    terraform_indicators = [
                        'terraform', 'provider', 'resource', 'data', 'variable',
                        'output', 'locals', 'module', 'backend'
                    ]
                    
                    if any(indicator in content for indicator in terraform_indicators):
                        return True
                        
            except Exception:
                pass
        
        return False
    
    def scan(self, file_path: str) -> Dict[str, Any]:
        """Perform security scan on Terraform file."""
        self._validate_file_exists(file_path)
        metadata = self._get_scan_metadata(file_path)
        
        scan_results = {
            "metadata": metadata,
            "scanner": "terraform_scanner",
            "tools": {}
        }
        
        # Run tfsec
        try:
            tfsec_result = self._run_tool("tfsec", file_path)
            scan_results["tools"]["tfsec"] = tfsec_result
        except Exception as e:
            scan_results["tools"]["tfsec"] = {
                "tool": "tfsec",
                "status": "error",
                "reason": str(e)
            }
        
        scan_results["overall_status"] = self._determine_overall_status(scan_results["tools"])
        return scan_results
    
    def get_description(self) -> str:
        """Get description of this scanner."""
        return "Terraform security scanner using tfsec"
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return [".tf", ".tfvars", ".hcl"]
    
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
