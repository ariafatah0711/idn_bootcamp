#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
import argparse

def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    report = f"# Audit Report\nGenerated: {datetime.utcnow()} UTC\n\n"

    trivy = load_json(outdir / "trivy_fs.json")
    if trivy:
        report += "## Trivy Findings\n"
        for r in trivy.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                report += f"- {v.get('VulnerabilityID')} ({v.get('Severity')}): {v.get('Title')}\n"

    checkov = load_json(outdir / "checkov.json")
    if checkov:
        report += "\n## Checkov Findings\n"
        if isinstance(checkov, dict):
            # Kalau memang dict, pakai cara lama
            failed_checks = checkov.get("results", {}).get("failed_checks", [])
            for c in failed_checks:
                report += f"- {c.get('check_id')} ({c.get('severity')}): {c.get('check_name')}\n"
        elif isinstance(checkov, list):
            # Kalau list, loop langsung
            for c in checkov:
                report += f"- {c.get('check_id')} ({c.get('severity')}): {c.get('check_name')}\n"

    (outdir / "report.md").write_text(report)
    print("Report generated:", outdir / "report.md")

if __name__ == "__main__":
    main()