# Security File Scanner - Modular Security Scanning Automation Tool

A modular Python application for automated security scanning of various infrastructure-as-code files including Dockerfiles, Kubernetes manifests, and Terraform configurations.

## Features

- **Modular Architecture**: Easy to add new scanners for different file types
- **Multiple Scanner Support**: 
  - Dockerfile scanning with hadolint and trivy
  - Kubernetes manifest scanning with kube-score
  - Terraform configuration scanning with tfsec and checkov
- **Flexible Output**: Save results to JSON files or output directories
- **Smart File Detection**: Automatically detects file types and applies appropriate scanners
- **Configuration Management**: JSON/YAML configuration files for scanner settings
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Prerequisites

### Required Tools

The following security scanning tools must be installed on your system:

#### Docker Scanner
- **hadolint**: Dockerfile linter (required)
- **trivy**: Container vulnerability scanner (optional)

#### Kubernetes Scanner
- **kube-score**: Kubernetes manifest security analyzer (required)

#### Terraform Scanner
- **tfsec**: Terraform security scanner (optional)
- **checkov**: Infrastructure as Code security scanner (optional)

### Installation Commands

#### Ubuntu/Debian
```bash
# Install hadolint
sudo wget -qO /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64
sudo chmod a+x /usr/local/bin/hadolint
hadolint --version

# Install trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install kube-score
sudo wget -qO /usr/local/bin/kube-score https://github.com/zegl/kube-score/releases/download/v1.20.0/kube-score_1.20.0_linux_amd64
sudo chmod a+x /usr/local/bin/kube-score
kube-score --version

# Install tfsec
curl -sSfL https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash

# Install checkov
pip install checkov
```

#### macOS
```bash
# Install hadolint
brew install hadolint

# Install trivy
brew install trivy

# Install kube-score
brew install kube-score

# Install tfsec
brew install tfsec

# Install checkov
pip install checkov
```

#### Windows
```bash
# Install via Chocolatey
choco install hadolint
choco install trivy
choco install kube-score
choco install tfsec

# Install checkov
pip install checkov
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd IacContainer
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python3 app.py list
```

## Usage

### Basic Commands

#### List Available Scanners
```bash
python3 app.py list
```

#### Scan a Single File
```bash
# Scan a Dockerfile
python3 app.py scan -f examples/Dockerfile

# Scan a Kubernetes manifest
python3 app.py scan -f examples/deployment.yaml

# Scan a Terraform file
python3 app.py scan -f examples/main.tf
```

#### Scan a Directory
```bash
# Scan all supported files in a directory
python3 app.py scan -f /path/to/project/
```

#### Save Results to File
```bash
# Save to specific JSON file
python3 app.py scan -f Dockerfile -o scan_results.json

# Save to output directory (auto-generates filename)
python3 app.py scan -f /path/to/project/ -o /output/dir/
```

### Examples

#### Scan Docker Project
```bash
# Scan a Docker project directory
python3 app.py scan -f ./docker-project/ -o ./scan-results/
```

#### Scan Kubernetes Project
```bash
# Scan Kubernetes manifests
python3 app.py scan -f ./k8s-manifests/ -o k8s-scan.json
```

#### Scan Terraform Project
```bash
# Scan Terraform configuration
python3 app.py scan -f ./terraform/ -o tf-scan.json
```

## Configuration

### Configuration File

The application uses `config.json` for scanner configuration. You can customize:

- Which scanners are active
- Tool command arguments
- Required vs optional tools
- Output settings

### Example Configuration

```json
{
  "scanners": {
    "docker_scanner": {
      "active": true,
      "tools": {
        "hadolint": {
          "command": "hadolint",
          "args": ["--format", "json"],
          "required": true
        }
      }
    }
  }
}
```

### Environment Variables

- `SECURITY_SCANNER_CONFIG`: Path to custom configuration file
- `SECURITY_SCANNER_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Architecture

### Core Components

1. **SecurityScannerApp** (`app.py`): Main application class handling CLI and orchestration
2. **ConfigManager** (`config_manager.py`): Configuration loading and management
3. **ScannerManager** (`scanner_manager.py`): Dynamic scanner loading and management
4. **BaseScanner** (`base_scanner.py`): Abstract base class for all scanners

### Scanner Modules

- **DockerScanner** (`scanners/docker_scanner.py`): Dockerfile security analysis
- **K8sScanner** (`scanners/k8s_scanner.py`): Kubernetes manifest security analysis
- **TerraformScanner** (`scanners/terraform_scanner.py`): Terraform configuration security analysis

### Adding New Scanners

1. Create a new scanner class in `scanners/` directory
2. Inherit from `BaseScanner`
3. Implement required abstract methods
4. Add configuration to `config.json`
5. The scanner will be automatically loaded

#### Example New Scanner

```python
# scanners/custom_scanner.py
from base_scanner import BaseScanner

class CustomScanner(BaseScanner):
    def can_scan_file(self, file_path, file_name, file_ext):
        # Implement file type detection
        pass
    
    def scan(self, file_path):
        # Implement scanning logic
        pass
    
    def get_description(self):
        return "Custom security scanner"
    
    def get_supported_extensions(self):
        return [".custom"]
    
    def get_required_tools(self):
        return ["custom-tool"]
```

## Output Format

### Scan Results Structure

```json
{
  "metadata": {
    "file_path": "/path/to/file",
    "file_name": "Dockerfile",
    "file_size": 1024,
    "file_type": "Dockerfile",
    "scanner": "docker_scanner",
    "timestamp": 1234567890
  },
  "scanner": "docker_scanner",
  "tools": {
    "hadolint": {
      "tool": "hadolint",
      "command": "hadolint --format json Dockerfile",
      "return_code": 0,
      "status": "success",
      "json_output": {...}
    }
  },
  "overall_status": "success"
}
```

### Status Values

- `success`: All tools completed successfully
- `partial_failure`: Some tools failed, others succeeded
- `failed`: All tools failed
- `no_tools_available`: No scanning tools are available

## Troubleshooting

### Common Issues

#### Tool Not Found
```
Error: Required tool 'hadolint' is not available
```
**Solution**: Install the missing tool using the installation commands above.

#### Permission Denied
```
Error: File not readable: /path/to/file
```
**Solution**: Check file permissions and ensure the application has read access.

#### Configuration Error
```
Warning: Could not load config file config.json
```
**Solution**: Verify the configuration file format and syntax.

### Debug Mode

Enable debug logging by setting the log level in configuration:

```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## Development

### Project Structure

```
IacContainer/
├── app.py                 # Main application
├── config_manager.py      # Configuration management
├── scanner_manager.py     # Scanner management
├── base_scanner.py        # Base scanner class
├── config.json           # Configuration file
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── scanners/            # Scanner modules
    ├── __init__.py
    ├── docker_scanner.py
    ├── k8s_scanner.py
    └── terraform_scanner.py
```

### Running Tests

```bash
# Run basic functionality test
python3 -c "from app import SecurityScannerApp; app = SecurityScannerApp(); app.list_scanners()"
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the configuration examples
3. Open an issue on GitHub
4. Check tool-specific documentation for CLI tool issues

## Roadmap

- [ ] Support for additional file types (Helm charts, Ansible playbooks)
- [ ] HTML/Markdown report generation
- [ ] Integration with CI/CD pipelines
- [ ] Web-based dashboard
- [ ] Custom rule configuration
- [ ] Severity-based filtering
- [ ] Historical scan comparison
