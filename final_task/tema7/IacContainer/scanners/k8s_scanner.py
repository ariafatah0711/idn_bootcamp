"""
Kubernetes Security Scanner

Scans Kubernetes manifests for security issues using kube-score.
"""

import os
import re
from typing import Dict, List, Any

from base_scanner import BaseScanner


class K8sScanner(BaseScanner):
    """
    Security scanner for Kubernetes manifests.
    
    Uses kube-score for Kubernetes security best practices validation.
    """
    
    def __init__(self, config_manager, scanner_name: str):
        """Initialize Kubernetes scanner."""
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
        # Check for common Kubernetes file extensions
        if file_ext in ['.yaml', '.yml', '.json']:
            # Check if file contains Kubernetes content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2048).lower()  # Read first 2KB
                    
                    # Look for Kubernetes API indicators
                    k8s_indicators = [
                        'apiVersion:', 'kind:', 'metadata:', 'spec:', 'status:',
                        'apiVersion: v1', 'apiVersion: apps/v1', 'apiVersion: networking.k8s.io/v1',
                        'kind: pod', 'kind: deployment', 'kind: service', 'kind: configmap',
                        'kind: secret', 'kind: ingress', 'kind: networkpolicy'
                    ]
                    
                    if any(indicator in content for indicator in k8s_indicators):
                        return True
                        
            except Exception:
                pass
        
        return False
    
    def scan(self, file_path: str) -> Dict[str, Any]:
        """
        Perform security scan on Kubernetes manifest.
        
        Args:
            file_path: Path to the Kubernetes manifest to scan
            
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
            "scanner": "k8s_scanner",
            "tools": {}
        }
        
        # Run kube-score
        try:
            kube_score_result = self._run_tool("kube_score", file_path)
            scan_results["tools"]["kube_score"] = kube_score_result
            
            # Add additional analysis if kube-score succeeded
            if kube_score_result.get("status") == "success":
                scan_results["k8s_analysis"] = self._analyze_k8s_content(file_path)
                
        except Exception as e:
            scan_results["tools"]["kube_score"] = {
                "tool": "kube_score",
                "status": "error",
                "reason": str(e)
            }
        
        # Determine overall scan status
        scan_results["overall_status"] = self._determine_overall_status(scan_results["tools"])
        
        return scan_results
    
    def get_description(self) -> str:
        """
        Get description of this scanner.
        
        Returns:
            Description string
        """
        return "Kubernetes manifest security scanner using kube-score"
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of supported file extensions.
        
        Returns:
            List of supported extensions
        """
        return [".yaml", ".yml", ".json"]
    
    def get_required_tools(self) -> List[str]:
        """
        Get list of required CLI tools.
        
        Returns:
            List of required tool names
        """
        return ["kube_score"]
    
    def _analyze_k8s_content(self, file_path: str) -> Dict[str, Any]:
        """
        Perform additional analysis of Kubernetes content.
        
        Args:
            file_path: Path to the Kubernetes manifest
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "resource_types": [],
            "security_concerns": [],
            "best_practices": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract resource types
                kind_pattern = r'kind:\s*(\w+)'
                kinds = re.findall(kind_pattern, content, re.IGNORECASE)
                analysis["resource_types"] = list(set(kinds))
                
                # Check for common security concerns
                security_patterns = {
                    "privileged_containers": r'privileged:\s*true',
                    "host_network": r'hostNetwork:\s*true',
                    "host_pid": r'hostPID:\s*true',
                    "host_ipc": r'hostIPC:\s*true',
                    "run_as_root": r'runAsNonRoot:\s*false',
                    "allow_privilege_escalation": r'allowPrivilegeEscalation:\s*true',
                    "read_only_root_filesystem": r'readOnlyRootFilesystem:\s*false'
                }
                
                for concern, pattern in security_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        analysis["security_concerns"].append(concern)
                
                # Check for best practices
                best_practice_patterns = {
                    "resource_limits": r'resources:\s*\n\s*limits:',
                    "resource_requests": r'resources:\s*\n\s*requests:',
                    "security_context": r'securityContext:',
                    "liveness_probe": r'livenessProbe:',
                    "readiness_probe": r'readinessProbe:',
                    "network_policy": r'kind:\s*NetworkPolicy'
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
