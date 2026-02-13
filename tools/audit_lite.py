#!/usr/bin/env python3
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

# Regex patterns for red flags
PATTERNS = {
    "curl_bash": r"(curl|wget).*?\|\s*(bash|sh)",
    "base64_decode_exec": r"(base64 -d|base64 --decode).*?\|\s*(bash|sh|python|perl|ruby)",
    "rm_rf_root": r"rm\s+(-rf|-fr|-r|-f)\s+/",
    "fork_bomb": r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;",
    "eval_exec": r"(eval|exec)\s*\(",
    "subprocess_shell": r"subprocess\..*?(shell\s*=\s*True)",
    "suspicious_domains": r"https?://[a-zA-Z0-9-]+\.(xyz|top|gq|cf|tk|ml|ga|cc)/",
    "hardcoded_secrets": r"(api_key|access_token|secret_key)\s*=\s*['\"][a-zA-Z0-9_\-]{20,}['\"]",
    "sudo_usage": r"sudo\s+",
    "chown_chmod_777": r"chmod\s+(-R\s+)?777"
}

def scan_file(file_path):
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.splitlines()
            
            for name, pattern in PATTERNS.items():
                # Global search
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    # Find line number
                    line_no = content[:match.start()].count('\n') + 1
                    snippet = lines[line_no-1].strip()[:100]
                    issues.append({
                        "type": name,
                        "file": str(file_path),
                        "line": line_no,
                        "snippet": snippet
                    })
    except Exception as e:
        issues.append({
            "type": "scan_error",
            "file": str(file_path),
            "line": 0,
            "snippet": str(e)
        })
    return issues

def generate_report(results, output_format="text"):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if output_format == "json":
        return json.dumps({"timestamp": timestamp, "results": results}, indent=2)
    
    report = [
        "==================================================",
        f" AI SECURITY AUDIT LITE - SCAN REPORT",
        f" Timestamp: {timestamp}",
        "==================================================",
        ""
    ]
    
    if not results:
        report.append("No critical red flags found.")
    else:
        file_map = {}
        for issue in results:
            f = issue['file']
            if f not in file_map:
                file_map[f] = []
            file_map[f].append(issue)
            
        for f, issues in file_map.items():
            report.append(f"FILE: {f}")
            for i in issues:
                report.append(f"  [!] {i['type'].upper()} at line {i['line']}")
                report.append(f"      Code: {i['snippet']}")
            report.append("")
            
    report.append("==================================================")
    report.append("DISCLAIMER: This is an automated static analysis.")
    report.append("It does not guarantee safety or catch logical flaws.")
    report.append("Manual review is required for verification.")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Audit Lite - Static Analysis for AI Skills")
    parser.add_argument("target", help="Directory or file to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Write report to file")
    
    args = parser.parse_args()
    
    target_path = Path(args.target)
    all_issues = []
    
    if target_path.is_file():
        all_issues.extend(scan_file(target_path))
    elif target_path.is_dir():
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.py', '.sh', '.md', '.js', '.ts', '.json')):
                     file_path = Path(root) / file
                     all_issues.extend(scan_file(file_path))
    else:
        print(f"Error: Target {target_path} not found.")
        return

    report = generate_report(all_issues, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()
