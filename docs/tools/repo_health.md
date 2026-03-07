# Repository Health Checker

Quick due diligence on any GitHub repository. Get a health score, activity metrics, and risk indicators in seconds.

## Features

- 📊 **Health Score** — 0-100 automated scoring
- 📈 **Activity Metrics** — Stars, forks, open issues
- ⚠️ **Risk Indicators** — Stale, archived, no license
- 📅 **Freshness Check** — Last commit date analysis
- 📜 **License Detection** — Identifies project license
- 🚀 **No API Key** — Uses public GitHub API

## Usage

```bash
# Basic health check
repo_health vercel/next.js

# Detailed output
repo_health facebook/react --details

# JSON for automation
repo_health owner/repo --json
```

## Health Score Algorithm

| Factor | Weight | Description |
|--------|--------|-------------|
| Stars | 25% | Community interest |
| Forks | 15% | Developer engagement |
| Recent Activity | 30% | Last commit < 90 days |
| Issues Ratio | 15% | Open vs closed ratio |
| Has License | 10% | Legal clarity |
| Not Archived | 5% | Active maintenance |

## Example Output

```
============================================================
📊 REPOSITORY HEALTH CHECK
============================================================

📍 Repository: vercel/next.js

🏥 Health Score: 94/100 EXCELLENT

📈 Statistics:
   ⭐ Stars: 112,847
   🍴 Forks: 23,456
   📋 Open Issues: 1,234
   ✅ Closed Issues: 45,678

📅 Activity:
   Last Commit: 2 days ago
   Status: 🟢 Active

📜 License: MIT
```

## Install

```bash
curl -fsSL https://barrowryan89-cloud.github.io/pd-researcher/tools/repo_health.py > repo_health
chmod +x repo_health
./repo_health vercel/next.js
```

---

Part of [PD's Free Developer Tools](https://barrowryan89-cloud.github.io/pd-researcher/)
