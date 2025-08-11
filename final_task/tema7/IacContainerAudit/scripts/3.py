#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
import argparse
import re

def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except:
        return None

def severity_class(sev):
    s = str(sev).upper()
    if s == "CRITICAL":
        return "critical"
    elif s == "HIGH":
        return "high"
    elif s == "MEDIUM" or s == "WARN":
        return "medium"
    elif s == "LOW":
        return "low"
    elif s == "INFO":
        return "info"
    return "unknown"

def make_table(rows, headers):
    if not rows:
        return "<p>No findings ✅</p>"
    html = "<table><tr>"
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr>"
    for row in rows:
        html += "<tr>"
        for i, cell in enumerate(row):
            if i == 1:  # severity column
                html += f"<td class='{severity_class(re.sub('<.*?>', '', str(cell)))}'>{cell}</td>"
            else:
                html += f"<td>{cell}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)

    # Collect data for summary
    severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}

    html = """<html>
<head>
<title>Security Audit Report</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
h1 { color: #333; }
.critical { color: white; background: red; padding: 3px 6px; border-radius: 4px; }
.high { color: white; background: darkorange; padding: 3px 6px; border-radius: 4px; }
.medium { color: black; background: gold; padding: 3px 6px; border-radius: 4px; }
.low { color: white; background: green; padding: 3px 6px; border-radius: 4px; }
.info { color: white; background: blue; padding: 3px 6px; border-radius: 4px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
th, td { border: 1px solid #ddd; padding: 8px; }
th { background-color: #f4f4f4; }
</style>
</head>
<body>
"""
    html += f"<h1>Security Audit Report</h1><p><strong>Generated:</strong> {datetime.utcnow()} UTC</p>"

    # Trivy
    trivy_rows = []
    trivy = load_json(outdir / "trivy_fs.json")
    if trivy:
        for r in trivy.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                sev = v.get("Severity", "UNKNOWN")
                severity_count[sev] = severity_count.get(sev, 0) + 1
                trivy_rows.append((
                    v.get("VulnerabilityID"),
                    sev,
                    v.get("Title")
                ))

    # Checkov
    checkov_rows = []
    checkov = load_json(outdir / "checkov.json")
    if checkov:
        if isinstance(checkov, list):
            for entry in checkov:
                if isinstance(entry, dict) and "results" in entry:
                    for fc in entry["results"].get("failed_checks", []):
                        checkov_rows.append((
                            fc.get("check_id"),
                            fc.get("check_name")
                        ))
        elif isinstance(checkov, dict):
            for fc in checkov.get("results", {}).get("failed_checks", []):
                checkov_rows.append((
                    fc.get("check_id"),
                    fc.get("check_name")
                ))

    # Dockle
    dockle_rows = []
    dockle = load_json(outdir / "dockle.json")
    if dockle and "details" in dockle:
        for d in dockle["details"]:
            sev = d.get("level", "UNKNOWN")
            severity_count[sev] = severity_count.get(sev, 0) + 1
            dockle_rows.append((
                d.get("code"),
                sev,
                d.get("title")
            ))

    # Summary table
    html += "<h2>Summary</h2><table>"
    html += "<tr><th>Severity</th><th>Count</th></tr>"
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        html += f"<tr><td class='{severity_class(sev)}'>{sev}</td><td>{severity_count.get(sev, 0)}</td></tr>"
    html += "</table>"

    # Per-tool details
    html += "<h2>Trivy Findings</h2>" + make_table(trivy_rows, ["ID", "Severity", "Title"])
    html += "<h2>Checkov Findings</h2>" + make_table(checkov_rows, ["Check ID", "Name"])
    html += "<h2>Dockle Findings</h2>" + make_table(dockle_rows, ["Code", "Level", "Title"])

    # Kube-score
    html += "<h2>Kube-score Findings</h2>"
    for file in outdir.glob("kubescore_*.txt"):
        html += f"<h3>{file.name}</h3><ul>"
        for line in file.read_text().splitlines():
            if "[CRITICAL]" in line:
                html += f"<li class='critical'>{line.strip()}</li>"
            elif "[WARNING]" in line:
                html += f"<li class='medium'>{line.strip()}</li>"
            elif line.strip():
                html += f"<li>{line.strip()}</li>"
        html += "</ul>"

    html += "</body></html>"

    # Save file
    (outdir / "report.html").write_text(html)
    print("HTML report generated:", outdir / "report.html")

if __name__ == "__main__":
    main()