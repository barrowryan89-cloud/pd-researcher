# Skill: Audit Lite (Security Scanner)

## Description
A lightweight static analysis tool designed to scan AI skills and scripts for common security red flags. It detects dangerous patterns like `curl|bash`, `rm -rf`, improper `subprocess` usage, and suspicious domains.

## Usage

Run the scanner against a specific file or an entire directory of skills.

### Basic Scan (Text Output)
```bash
python3 tools/audit_lite.py /path/to/skills/folder
```

### JSON Output (for programmatic parsing)
```bash
python3 tools/audit_lite.py /path/to/skills/folder --format json
```

### Save Report to File
```bash
python3 tools/audit_lite.py /path/to/skills/folder --output report.txt
```

## Detection Capabilities
The tool scans for regex patterns including but not limited to:
- **Remote Execution:** `curl|bash`, `wget|sh`
- **Obfuscation:** `base64` decode piped to execution
- **Destructive Commands:** `rm -rf /`, fork bombs
- **Unsafe Python:** `eval()`, `exec()`, `subprocess(shell=True)`
- **Suspicious Networking:** Known sketchy TLDs (.xyz, .top, etc.)
- **Permissions:** `chmod 777`, `sudo` usage
- **Secrets:** Potential hardcoded API keys

## Disclaimer
**"Audit Lite" is a first-pass static analysis tool.** 
- It is **NOT** a replacement for a professional security audit.
- It produces **False Positives** (matches that are actually safe) and **False Negatives** (misses sophisticated attacks).
- Use this as a helper to triage code, not as a final stamp of approval.
