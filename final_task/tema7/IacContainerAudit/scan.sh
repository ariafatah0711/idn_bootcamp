#!/usr/bin/env bash
set -euo pipefail

WORKDIR=/app
APP=workspace/2
OUTDIR="$WORKDIR/outputs"
mkdir -p "$OUTDIR"

echo "Running Trivy FS scan..."
trivy fs --format json --output "$OUTDIR/trivy_fs.json" "$WORKDIR/$APP" || true

echo "Running Checkov..."
# checkov -d "$WORKDIR/$APP" --output json > "$OUTDIR/checkov.json" || true
checkov -d "$WORKDIR/$APP" --output json --compact > "$OUTDIR/checkov.json" || true
# checkov -d "$WORKDIR/$APP" --output cyclonedx_json --compact > "$OUTDIR/checkov.json" || true

echo "Running tfsec..."
if command -v tfsec >/dev/null 2>&1; then
    tfsec --format json --out "$OUTDIR/tfsec.json" "$WORKDIR/$APP" || true
else
    echo "tfsec not found, skipping..."
fi

echo "Running Dockle..."
if command -v docker >/dev/null 2>&1; then
    docker build -t test-image "$WORKDIR/$APP" || true
    dockle --format json --output "$OUTDIR/dockle.json" test-image || true
else
    echo "Docker CLI not found in container."
fi

echo "Running kube-score..."
for f in $(find "$WORKDIR/$APP" -name "*.yaml" -o -name "*.yml"); do
    kube-score score "$f" > "$OUTDIR/kubescore_$(basename "$f").txt" || true
done

python3 "$WORKDIR/scripts/reporter.py" --outdir "$OUTDIR"
echo "All done. Check $OUTDIR"
