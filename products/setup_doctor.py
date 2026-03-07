#!/usr/bin/env python3
"""PD Setup Doctor - quick health check for an OpenClaw workspace + host.

Outputs:
- Plain text report (default)
- JSON report (--json)

This is intentionally lightweight and safe: read-only checks only.
"""

import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def sh(cmd):
    try:
        p = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:
        return 99, "", str(e)


def exists(path):
    return Path(path).expanduser().exists()


def check_file(path, max_bytes=20000):
    p = Path(path).expanduser()
    if not p.exists():
        return {"exists": False}
    try:
        data = p.read_text(errors="ignore")
        return {"exists": True, "bytes": len(data.encode("utf-8")), "head": data[:max_bytes]}
    except Exception as e:
        return {"exists": True, "error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=str(Path.cwd()))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    ws = Path(args.workspace).expanduser().resolve()

    report = {
        "timestamp": ts,
        "workspace": str(ws),
        "checks": {}
    }

    # OS basics
    rc, out, err = sh("uptime")
    report["checks"]["uptime"] = {"rc": rc, "out": out, "err": err}

    rc, out, err = sh("free -h")
    report["checks"]["memory"] = {"rc": rc, "out": out, "err": err}

    rc, out, err = sh("df -h")
    report["checks"]["disk"] = {"rc": rc, "out": out, "err": err}

    # OpenClaw file structure sanity
    report["checks"]["paths"] = {
        "MEMORY.md": exists(ws / "MEMORY.md"),
        "memory_dir": exists(ws / "memory"),
        "products_dir": exists(ws / "products"),
        "skills_dir": exists(ws / "skills"),
        "tools_dir": exists(ws / "tools"),
        "HEARTBEAT.md": exists(ws / "HEARTBEAT.md"),
    }

    # Recent daily memory file
    today = datetime.utcnow().strftime("%Y-%m-%d")
    report["checks"]["daily_memory"] = check_file(ws / "memory" / f"{today}.md")

    # Gateway config exists
    report["checks"]["openclaw_config"] = check_file(Path("~/.openclaw/openclaw.json"))

    # Cron jobs summary (requires gateway up; best-effort)
    try:
        from subprocess import run
        # We can't call openclaw CLI here (may not be in PATH). So just note that.
        report["checks"]["cron"] = {"note": "Cron jobs managed by gateway; verify via gateway UI/logs."}
    except Exception as e:
        report["checks"]["cron"] = {"error": str(e)}

    # Twilio env presence (do not print secrets)
    report["checks"]["twilio_env"] = {
        "TWILIO_ACCOUNT_SID": bool(os.getenv("TWILIO_ACCOUNT_SID")),
        "TWILIO_AUTH_TOKEN": bool(os.getenv("TWILIO_AUTH_TOKEN")),
        "TWILIO_FROM_NUMBER": bool(os.getenv("TWILIO_FROM_NUMBER")),
        "TWILIO_TO_NUMBER": bool(os.getenv("TWILIO_TO_NUMBER")),
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return

    # Plain text render
    lines = []
    lines.append("PD SETUP DOCTOR")
    lines.append(f"Timestamp: {ts}")
    lines.append(f"Workspace: {ws}")
    lines.append("")

    lines.append("SYSTEM")
    lines.append(report["checks"]["uptime"]["out"] or "(uptime unavailable)")
    lines.append("")

    lines.append("MEMORY/DIRS")
    for k, v in report["checks"]["paths"].items():
        lines.append(f"- {k}: {'OK' if v else 'MISSING'}")
    lines.append("")

    dm = report["checks"]["daily_memory"]
    if dm.get("exists"):
        lines.append(f"Daily memory file: OK ({dm.get('bytes','?')} bytes)")
    else:
        lines.append("Daily memory file: MISSING")

    lines.append("")
    lines.append("NOTES")
    lines.append("- This tool is read-only. Use it to diagnose reliability before selling Setup-as-a-Service.")
    lines.append("- If you see OOMs, lower concurrency and/or add swap.")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
