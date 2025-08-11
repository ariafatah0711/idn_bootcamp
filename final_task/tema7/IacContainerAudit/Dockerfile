FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl bash git docker.io \
    && rm -rf /var/lib/apt/lists/*

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Install Dockle
RUN curl -sSL https://github.com/goodwithtech/dockle/releases/download/v0.4.15/dockle_0.4.15_Linux-386.tar.gz \
    | tar zx -C /usr/local/bin

# Install kube-score
RUN curl -sSL https://github.com/zegl/kube-score/releases/download/v1.20.0/kube-score_1.20.0_linux_amd64.tar.gz \
    | tar zx -C /usr/local/bin

# Install Checkov
RUN pip install --no-cache-dir checkov

# Install tfsec
RUN curl -sSL https://github.com/aquasecurity/tfsec/releases/latest/download/tfsec-linux-amd64 \
    -o /usr/local/bin/tfsec && chmod +x /usr/local/bin/tfsec

# Buat folder project
WORKDIR /app

# Copy file script, and sh
COPY ./scripts/reporter.py scripts/
COPY ./scan.sh .
RUN ls

# Set permission
RUN chmod +x scan.sh

# Entrypoint untuk jalankan scan
ENTRYPOINT ["bash", "scan.sh"]