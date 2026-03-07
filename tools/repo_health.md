# repo_health

Quick health check for any GitHub repository. One command, instant insights.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/tools/repo_health.py | python3 - owner/repo
```

Or download and run locally:

```bash
wget https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/tools/repo_health.py
chmod +x repo_health.py
./repo_health.py facebook/react --details
```

## Usage

```bash
repo_health <owner/repo> [--details]
```

## Examples

```bash
# Quick health check
repo_health vercel/next.js

# Full details
repo_health microsoft/vscode --details

# Check your own repos
repo_health barrowryan89-cloud/pd-researcher
```

## Output

```
🟢 vercel/next.js
==================================================
📊 Health Score: 80/100
⭐ Stars: 137.7K
🍴 Forks: 30.5K
🐛 Open Issues: 3.3K
📝 Last Push: 🟢 Active 1d ago
🔤 Language: JavaScript
⚖️  License: MIT
```

## Health Score Algorithm

- Base: 50 points
- Popularity: +5 to +15 (based on stars)
- Activity: +5 to +15 (based on last push)
- Metadata: +5 (description), +5 (topics), +5 (license)
- Penalties: -5 to -10 (too many open issues), -10 (stale >90 days)

## Why?

Before depending on a library or contributing to a project:
- Is it actively maintained?
- Is it popular/well-tested?
- Is it properly licensed?
- Are issues being addressed?

**No API key required.** Uses GitHub's public API (rate limited).

---

Part of [PD Researcher](https://barrowryan89-cloud.github.io/pd-researcher/) — 50+ free CLI tools for developers.
