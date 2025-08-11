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

def severity_color(sev):
    colors = {
        "CRITICAL": "red",
        "HIGH": "darkred",
        "MEDIUM": "orange",
        "LOW": "green",
        "INFO": "blue"
    }
    return colors.get(str(sev).upper(), "black")

def make_table(rows, headers):
    if not rows:
        return "<p><em>No findings</em></p>"
    table = "<table border='1' cellpadding='5' cellspacing='0'><tr>"
    for h in headers:
        table += f"<th>{h}</th>"
    table += "</tr>"
    for row in rows:
        table += "<tr>"
        for cell in row:
            table += f"<td>{cell}</td>"
        table += "</tr>"
    table += "</table>"
    return table

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    html = f"<html><head><title>Audit Report</title></head><body>"
    html += f"<h1>Audit Report</h1><p>Generated: {datetime.utcnow()} UTC</p>"

    # Trivy
    html += "<h2>Trivy Findings</h2>"
    trivy = load_json(outdir / "trivy_fs.json")
    trivy_rows = []
    if trivy:
        for r in trivy.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                sev = v.get("Severity", "UNKNOWN")
                trivy_rows.append((
                    v.get("VulnerabilityID"),
                    f"<span style='color:{severity_color(sev)}'>{sev}</span>",
                    v.get("Title")
                ))
    html += make_table(trivy_rows, ["ID", "Severity", "Title"])

    # Checkov
    html += "<h2>Checkov Findings</h2>"
    checkov = load_json(outdir / "checkov.json")
    checkov_rows = []
    if checkov:
        if isinstance(checkov, dict):
            failed_checks = checkov.get("results", {}).get("failed_checks", [])
            for c in failed_checks:
                sev = c.get("severity", "UNKNOWN")
                checkov_rows.append((
                    c.get("check_id"),
                    f"<span style='color:{severity_color(sev)}'>{sev}</span>",
                    c.get("check_name")
                ))
        elif isinstance(checkov, list):
            for c in checkov:
                sev = c.get("severity", "UNKNOWN")
                checkov_rows.append((
                    c.get("check_id"),
                    f"<span style='color:{severity_color(sev)}'>{sev}</span>",
                    c.get("check_name")
                ))
    html += make_table(checkov_rows, ["Check ID", "Severity", "Name"])

    # Dockle
    html += "<h2>Dockle Findings</h2>"
    dockle = load_json(outdir / "dockle.json")
    dockle_rows = []
    if dockle and "details" in dockle:
        for d in dockle["details"]:
            sev = d.get("level", "UNKNOWN")
            dockle_rows.append((
                d.get("code"),
                f"<span style='color:{severity_color(sev)}'>{sev}</span>",
                d.get("title")
            ))
    html += make_table(dockle_rows, ["Code", "Level", "Title"])

    # kube-score
    html += "<h2>Kube-score Findings</h2>"
    for file in outdir.glob("kubescore_*.txt"):
        html += f"<h3>{file.name}</h3><pre>{file.read_text()}</pre>"

    html += "</body></html>"

    (outdir / "report.html").write_text(html)
    print("HTML report generated:", outdir / "report.html")

if __name__ == "__main__":
    main()