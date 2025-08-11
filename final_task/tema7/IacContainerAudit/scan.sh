#!/usr/bin/env bash
set -euo pipefail

WORKDIR=/app
OUTDIR="$WORKDIR/outputs"
mkdir -p "$OUTDIR"

echo "Running Trivy FS scan..."
trivy fs --format json --output "$OUTDIR/trivy_fs.json" "$WORKDIR/workspace" || true

echo "Running Checkov..."
checkov -d "$WORKDIR/workspace" --output json > "$OUTDIR/checkov.json" || true

echo "Running Dockle..."
if command -v docker >/dev/null 2>&1; then
    docker build -t test-image "$WORKDIR/workspace" || true
    dockle --format json --output "$OUTDIR/dockle.json" test-image || true
else
    echo "Docker CLI not found in container."
fi

echo "Running kube-score..."
for f in $(find "$WORKDIR/workspace" -name "*.yaml" -o -name "*.yml"); do
    kube-score score "$f" > "$OUTDIR/kubescore_$(basename "$f").txt" || true
done

python3 "$WORKDIR/scripts/reporter.py" --outdir "$OUTDIR"
echo "All done. Check $OUTDIR"
