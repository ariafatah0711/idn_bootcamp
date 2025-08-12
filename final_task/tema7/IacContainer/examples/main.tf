# Sample Terraform configuration with security issues for testing
# This file contains intentional security problems for demonstration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Security issue: No backend configuration for state management
# Security issue: No encryption configuration

provider "aws" {
  region = "us-east-1"
  # Security issue: No explicit credentials management
}

# Security issue: Public S3 bucket
resource "aws_s3_bucket" "public_bucket" {
  bucket = "my-public-bucket-12345"
  
  # Security issue: No encryption
  # Security issue: No versioning
  # Security issue: No logging
}

# Security issue: Public access block disabled
resource "aws_s3_bucket_public_access_block" "public_bucket" {
  bucket = aws_s3_bucket.public_bucket.id
  
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Security issue: Public bucket policy
resource "aws_s3_bucket_policy" "public_bucket" {
  bucket = aws_s3_bucket.public_bucket.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.public_bucket.arn}/*"
      },
    ]
  })
}

# Security issue: EC2 instance with public IP
resource "aws_instance" "web_server" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  # Security issue: Public IP enabled
  associate_public_ip_address = true
  
  # Security issue: No encryption for root volume
  root_block_device {
    volume_size = 20
    volume_type = "gp2"
    # Security issue: No encryption
    encrypted = false
  }
  
  # Security issue: No IAM role
  # Security issue: No security groups
  
  tags = {
    Name = "WebServer"
    Environment = "Production"
  }
}

# Security issue: Security group with open access
resource "aws_security_group" "open_sg" {
  name        = "open-security-group"
  description = "Security group with open access"
  vpc_id      = "vpc-12345678"
  
  # Security issue: Open ingress rule
  ingress {
    description = "Open SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Security issue: Open HTTP access
  ingress {
    description = "Open HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Security issue: Open HTTPS access
  ingress {
    description = "Open HTTPS access"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Security issue: Open egress rule
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "OpenSecurityGroup"
  }
}

# Security issue: RDS instance with public access
resource "aws_db_instance" "database" {
  identifier = "my-database"
  
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  storage_type         = "gp2"
  storage_encrypted    = false  # Security issue: No encryption
  
  db_name  = "mydb"
  username = "dbadmin"
  password = "insecure-password"  # Security issue: Plain text password
  
  # Security issue: Publicly accessible
  publicly_accessible = true
  
  # Security issue: No backup retention
  backup_retention_period = 0
  
  # Security issue: No deletion protection
  deletion_protection = false
  
  tags = {
    Name = "MyDatabase"
  }
}

# Security issue: IAM user with excessive permissions
resource "aws_iam_user" "admin_user" {
  name = "admin-user"
  
  tags = {
    Name = "AdminUser"
  }
}

# Security issue: Admin policy attachment
resource "aws_iam_user_policy_attachment" "admin_policy" {
  user       = aws_iam_user.admin_user.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# Security issue: No MFA requirement
# Security issue: No password policy
# Security issue: No access key rotation

# Variables without validation
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
  
  # Security issue: No validation rules
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  
  # Security issue: No validation rules
}

# Outputs without sensitive marking
output "database_endpoint" {
  value = aws_db_instance.database.endpoint
  
  # Security issue: Not marked as sensitive
}

output "s3_bucket_name" {
  value = aws_s3_bucket.public_bucket.bucket
  
  # Security issue: Not marked as sensitive
}

# Security issue: No tags for cost tracking
# Security issue: No monitoring configuration
# Security issue: No logging configuration
# Security issue: No backup strategy
