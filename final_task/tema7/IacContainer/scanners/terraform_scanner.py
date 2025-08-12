"""
Terraform Security Scanner

Scans Terraform files for security issues using tfsec and checkov.
"""

import os
import re
from typing import Dict, List, Any

from base_scanner import BaseScanner


class TerraformScanner(BaseScanner):
    """
    Security scanner for Terraform files.
    
    Uses tfsec and checkov for Terraform security scanning.
    """
    
    def __init__(self, config_manager, scanner_name: str):
        """Initialize Terraform scanner."""
        super().__init__(config_manager, scanner_name)
    
    def can_scan_file(self, file_path: str, file_name: str, file_ext: str) -> bool:
        """
        Check if this scanner can handle the given file.
        
        Args:
            file_path: Full path to the file
            file_name: Name of the file
            file_ext: File extension (with dot)
            
        Returns:
            True if this scanner can scan the file, False otherwise
        """
        # Check for Terraform file extensions
        if file_ext in ['.tf', '.tfvars', '.hcl']:
            return True
        
        # Check if file contains Terraform content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2048).lower()  # Read first 2KB
                
                # Look for Terraform indicators
                terraform_indicators = [
                    'terraform {', 'provider "', 'resource "', 'data "',
                    'variable "', 'output "', 'module "', 'locals {',
                    'terraform_version', 'required_version', 'required_providers'
                ]
                
                if any(indicator in content for indicator in terraform_indicators):
                    return True
                    
        except Exception:
            pass
        
        return False
    
    def scan(self, file_path: str) -> Dict[str, Any]:
        """
        Perform security scan on Terraform file.
        
        Args:
            file_path: Path to the Terraform file to scan
            
        Returns:
            Dictionary containing scan results
        """
        # Validate file
        self._validate_file_exists(file_path)
        
        # Get metadata
        metadata = self._get_scan_metadata(file_path)
        
        # Initialize results
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
        
        # Run checkov
        try:
            checkov_result = self._run_tool("checkov", file_path)
            scan_results["tools"]["checkov"] = checkov_result
        except Exception as e:
            scan_results["tools"]["checkov"] = {
                "tool": "checkov",
                "status": "error",
                "reason": str(e)
            }
        
        # Add additional analysis if any tools succeeded
        if any(tool.get("status") == "success" for tool in scan_results["tools"].values()):
            scan_results["terraform_analysis"] = self._analyze_terraform_content(file_path)
        
        # Determine overall scan status
        scan_results["overall_status"] = self._determine_overall_status(scan_results["tools"])
        
        return scan_results
    
    def get_description(self) -> str:
        """
        Get description of this scanner.
        
        Returns:
            Description string
        """
        return "Terraform security scanner using tfsec and checkov"
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of supported file extensions.
        
        Returns:
            List of supported extensions
        """
        return [".tf", ".tfvars", ".hcl"]
    
    def get_required_tools(self) -> List[str]:
        """
        Get list of required CLI tools.
        
        Returns:
            List of required tool names
        """
        return ["tfsec", "checkov"]
    
    def _analyze_terraform_content(self, file_path: str) -> Dict[str, Any]:
        """
        Perform additional analysis of Terraform content.
        
        Args:
            file_path: Path to the Terraform file
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "resource_types": [],
            "providers": [],
            "security_concerns": [],
            "best_practices": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract resource types
                resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
                resources = re.findall(resource_pattern, content, re.IGNORECASE)
                analysis["resource_types"] = [f"{resource_type}.{resource_name}" for resource_type, resource_name in resources]
                
                # Extract data sources
                data_pattern = r'data\s+"([^"]+)"\s+"([^"]+)"'
                data_sources = re.findall(data_pattern, content, re.IGNORECASE)
                analysis["resource_types"].extend([f"data.{data_type}.{data_name}" for data_type, data_name in data_sources])
                
                # Extract providers
                provider_pattern = r'provider\s+"([^"]+)"'
                providers = re.findall(provider_pattern, content, re.IGNORECASE)
                analysis["providers"] = list(set(providers))
                
                # Check for common security concerns
                security_patterns = {
                    "public_access": r'cidr_blocks\s*=\s*\[.*"0\.0\.0\.0/0"',
                    "unencrypted_storage": r'encryption\s*{\s*enabled\s*=\s*false',
                    "public_buckets": r'public_access_block\s*{\s*block_public_access\s*=\s*false',
                    "weak_crypto": r'algorithm\s*=\s*"md5"',
                    "exposed_secrets": r'password\s*=\s*"[^"]*"',
                    "unrestricted_ingress": r'cidr_blocks\s*=\s*\[.*"0\.0\.0\.0/0"',
                    "unrestricted_egress": r'cidr_blocks\s*=\s*\[.*"0\.0\.0\.0/0"'
                }
                
                for concern, pattern in security_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        analysis["security_concerns"].append(concern)
                
                # Check for best practices
                best_practice_patterns = {
                    "version_constraints": r'required_version\s*=\s*"[^"]*"',
                    "provider_constraints": r'required_providers\s*{',
                    "backends": r'backend\s+"[^"]*"',
                    "variables": r'variable\s+"[^"]*"',
                    "outputs": r'output\s+"[^"]*"',
                    "locals": r'locals\s*{',
                    "tags": r'tags\s*=\s*{'
                }
                
                for practice, pattern in best_practice_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        analysis["best_practices"].append(practice)
                        
        except Exception as e:
            analysis["error"] = f"Could not analyze content: {str(e)}"
        
        return analysis
    
    def _determine_overall_status(self, tools_results: Dict[str, Any]) -> str:
        """
        Determine overall scan status based on tool results.
        
        Args:
            tools_results: Results from all tools
            
        Returns:
            Overall status string
        """
        if not tools_results:
            return "no_tools_available"
        
        # Check if any tools failed
        failed_tools = [
            tool for tool, result in tools_results.items()
            if result.get("status") == "failed"
        ]
        
        if failed_tools:
            return "partial_failure"
        
        # Check if any tools succeeded
        successful_tools = [
            tool for tool, result in tools_results.items()
            if result.get("status") == "success"
        ]
        
        if successful_tools:
            return "success"
        
        return "no_tools_available"
