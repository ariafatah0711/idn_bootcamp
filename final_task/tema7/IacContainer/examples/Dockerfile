# Sample Dockerfile with security issues for testing
# This file contains intentional security problems for demonstration

# Use a base image without specifying version (security issue)
FROM ubuntu

# Run as root (security issue)
USER root

# Install packages without cleanup (security issue)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY app.py /app/
COPY requirements.txt /app/

# Set working directory
WORKDIR /app

# Expose port without security context
EXPOSE 8080

# Run application as root (security issue)
CMD ["python", "app.py"]

# Add some additional layers for testing
RUN echo "This is a test layer" > /tmp/test.txt

# Use ADD instead of COPY (security issue)
ADD https://example.com/file.txt /tmp/

# Create a user but don't use it
RUN useradd -m testuser
# USER testuser  # Commented out - still running as root

# Health check without proper configuration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
