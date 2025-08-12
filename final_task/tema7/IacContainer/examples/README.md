# Security Scanner Examples

This folder contains sample files with intentional security issues for testing the security scanner application.

## ⚠️ WARNING

**These files contain intentional security vulnerabilities and should NEVER be used in production environments!**

They are designed solely for testing and demonstrating the security scanning capabilities.

## Files Overview

### 1. `Dockerfile`
A Dockerfile with multiple security issues including:
- Running as root user
- Using base image without version pinning
- Using ADD instead of COPY
- No user switching
- Insecure health check configuration

**Security Issues Detected:**
- `privileged_containers`
- `run_as_root`
- `allow_privilege_escalation`
- `read_only_root_filesystem`

### 2. `deployment.yaml`
A Kubernetes deployment with security vulnerabilities:
- Privileged containers
- Running as root
- Host networking enabled
- Host volume mounts
- No resource limits
- Insecure security contexts

**Security Issues Detected:**
- `privileged_containers`
- `host_network`
- `host_pid`
- `host_ipc`
- `run_as_root`
- `allow_privilege_escalation`

### 3. `main.tf`
A Terraform configuration with AWS security problems:
- Public S3 bucket access
- Open security groups (0.0.0.0/0)
- Unencrypted storage
- Publicly accessible RDS
- Excessive IAM permissions
- Plain text passwords

**Security Issues Detected:**
- `public_access`
- `unencrypted_storage`
- `public_buckets`
- `exposed_secrets`
- `unrestricted_ingress`
- `unrestricted_egress`

## Testing the Scanner

### Test Individual Files
```bash
# Test Dockerfile
python3 ../app.py scan -f Dockerfile

# Test Kubernetes deployment
python3 ../app.py scan -f deployment.yaml

# Test Terraform configuration
python3 ../app.py scan -f main.tf
```

### Test All Examples
```bash
# Scan entire examples directory
python3 ../app.py scan -f . -o ../scan-results/
```

### Expected Results

Each file should trigger multiple security warnings from their respective scanners:

- **Dockerfile**: hadolint and trivy should detect multiple issues
- **deployment.yaml**: kube-score should identify security misconfigurations
- **main.tf**: tfsec and checkov should flag multiple security violations

## Learning Objectives

These examples demonstrate:

1. **Common Security Misconfigurations** in infrastructure code
2. **Scanner Detection Capabilities** for different file types
3. **Real-world Security Issues** that developers might accidentally introduce
4. **Best Practices** through negative examples

## Remediation Examples

### Dockerfile Fixes
```dockerfile
# Use specific base image version
FROM ubuntu:22.04

# Create non-root user
RUN useradd -m -u 1000 appuser

# Switch to non-root user
USER appuser

# Use COPY instead of ADD
COPY app.py /app/
```

### Kubernetes Fixes
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
  
  containers:
  - name: app
    securityContext:
      privileged: false
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
```

### Terraform Fixes
```hcl
# Encrypt S3 bucket
resource "aws_s3_bucket" "secure_bucket" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.secure_bucket.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Restrict security group access
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]  # Private network only
}
```

## Security Best Practices

1. **Principle of Least Privilege**: Only grant necessary permissions
2. **Defense in Depth**: Multiple layers of security controls
3. **Secure by Default**: Start with secure configurations
4. **Regular Scanning**: Integrate security scanning in CI/CD pipelines
5. **Documentation**: Document security decisions and configurations

## Next Steps

After testing with these examples:

1. **Review Scanner Output**: Understand what each scanner detects
2. **Fix Issues**: Practice remediating the security problems
3. **Create Secure Versions**: Build secure alternatives to these examples
4. **Integrate Scanning**: Add security scanning to your development workflow
5. **Customize Rules**: Configure scanners for your specific security requirements
