# Security File Scanner

A modular Python application for automated security scanning of infrastructure-as-code files.

## Features

- **Modular Design**: Easy to add new scanners
- **Multiple File Types**: Docker, Kubernetes, Terraform
- **CLI Interface**: Simple command-line usage
- **JSON Output**: Structured scan results
- **Configuration Management**: YAML/JSON config support

## Supported Scanners

| Scanner | Tools | File Types |
|---------|-------|------------|
| **Docker** | hadolint, trivy | Dockerfile, .dockerfile |
| **Kubernetes** | kube-score | .yaml, .yml, .json |
| **Terraform** | tfsec | .tf, .tfvars, .hcl |

## Installation

### Prerequisites

Install the required security tools:

```bash
# Docker scanning
sudo apt-get install hadolint
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Kubernetes scanning
curl -sSfL https://raw.githubusercontent.com/zegl/kube-score/master/install.sh | sh

# Terraform scanning
curl -sfL https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install.sh | sh
```

### Application Setup

```bash
# Clone the repository
git clone <repository-url>
cd IacContainer

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### List Available Scanners

```bash
python3 app.py list
```

### Scan Individual Files

```bash
# Scan Dockerfile
python3 app.py scan -f examples/Dockerfile

# Scan Kubernetes manifest
python3 app.py scan -f examples/deployment.yaml

# Scan Terraform file
python3 app.py scan -f examples/main.tf
```

### Scan Directories

```bash
# Scan entire examples directory
python3 app.py scan -f examples/ -o scan-results/

# Save to specific file
python3 app.py scan -f examples/ -o results.json
```

## Configuration

The application uses `config.json` for scanner configuration. Each scanner defines:

- **active**: Whether the scanner is enabled
- **tools**: CLI tools and their arguments
- **extensions**: Supported file extensions

Example:
```json
{
  "scanners": {
    "docker_scanner": {
      "active": true,
      "tools": {
        "hadolint": {
          "command": "hadolint",
          "args": ["--format", "json", "PLACEHOLDER"],
          "required": true
        }
      }
    }
  }
}
```

## Architecture

```
app.py                 # Main CLI application
├── config_manager.py  # Configuration management
├── scanner_manager.py # Scanner loading and management
├── base_scanner.py    # Abstract scanner interface
└── scanners/          # Individual scanner implementations
    ├── docker_scanner.py
    ├── k8s_scanner.py
    └── terraform_scanner.py
```

## Adding New Scanners

1. Create a new scanner class in `scanners/`
2. Inherit from `BaseScanner`
3. Implement required abstract methods
4. Add configuration to `config.json`
5. The scanner will be automatically loaded

## Output Format

Scan results include:

- **metadata**: File information and scan details
- **tools**: Results from each security tool
- **overall_status**: Overall scan status

Example output:
```json
{
  "metadata": {
    "file_path": "examples/Dockerfile",
    "file_type": "Dockerfile",
    "scanner": "docker_scanner"
  },
  "tools": {
    "hadolint": {
      "status": "success",
      "command": "hadolint --format json examples/Dockerfile"
    }
  },
  "overall_status": "success"
}
```

## Troubleshooting

### Common Issues

1. **"Tool not available"**: Install the required security tool
2. **"No configuration found"**: Check `config.json` format
3. **Permission errors**: Ensure file read permissions

### Debug Mode

For detailed error information, check the tool output in scan results.

## Development

### Code Structure

- **Clean Architecture**: Separation of concerns
- **Type Hints**: Full Python type annotations
- **Error Handling**: Graceful error handling
- **Modular Design**: Easy to extend and maintain

### Testing

```bash
# Test basic functionality
python3 app.py list

# Test scanner loading
python3 app.py scan -f examples/Dockerfile
```

## License

This project is licensed under the MIT License.
