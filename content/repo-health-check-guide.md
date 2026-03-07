# How to Evaluate Open Source Dependencies (Before They Burn You)

**One command to know if a GitHub repo is safe to depend on.**

Every developer has been there. You find a perfect library on GitHub. It solves your exact problem. The README looks professional. You `npm install` it (or `pip install`, `cargo add`, whatever).

Three months later:
- Critical security vulnerability discovered
- No maintainer response for weeks
- You're now maintaining a fork you never wanted

## The Hidden Cost of Bad Dependencies

According to [Synopsys' 2024 report](https://www.synopsys.com/software-integrity/report/open-source-security-risk-analysis.html), 96% of codebases contain open source. And 74% of those have high-risk vulnerabilities.

But security isn't the only risk:

| Risk | Impact | Detection |
|------|--------|-----------|
| **Abandoned** | No bug fixes, no updates | Check last commit date |
| **Under-licensed** | Legal exposure | Check LICENSE file |
| **Low activity** | Slow bug fixes | Check commit frequency |
| **Bus factor = 1** | Single point of failure | Check contributor count |
| **Reputation risk** | Depends on something sketchy | Check stars, forks, issues |

## Manual Due Diligence is Painful

Before adding a dependency, you *should* check:
- ⭐ Stars (social proof + longevity indicator)
- 🍴 Forks (community engagement)
- 🐛 Open issues vs. closed (maintenance health)
- 📅 Last commit (is it maintained?)
- 📜 License (can you legally use it?)
- 👥 Contributors (bus factor)

That's 6+ clicks per repo. For a typical project evaluating 20+ dependencies, you're looking at **100+ clicks and 30+ minutes** of manual work.

## The 1-Command Solution

I built `repo_health` to automate this. It's a zero-dependency CLI that gives you a 0-100 health score for any public GitHub repo:

```bash
repo_health facebook/react
```

Output:
```
🔍 Repo Health: facebook/react
🟢 Health Score: 98/100
======================================

⭐ 230K stars  🍴 48K forks  👁️ 6.7K watchers

📊 Activity:
   Commits (2024): 1,847  📈
   Open Issues: 1,203  🐛
   Open PRs: 312  🔀

📅 Last commit: 2 hours ago ✅
📝 License: MIT ✅

Health: EXCELLENT — Actively maintained, high activity
```

### What the Score Means

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 80-100 | 🟢 Excellent | Safe to depend on |
| 60-79 | 🟡 Good | Probably fine, monitor |
| 40-59 | 🟠 Fair | Use with caution |
| 20-39 | 🔴 Poor | High risk |
| 0-19 | ⚫ Critical | Avoid |

## Real Examples

**A healthy dependency:**
```bash
$ repo_health vercel/next.js --details
🟢 Health Score: 94/100
Last commit: 4 hours ago
License: MIT
Stars: 127K | Forks: 27K
Assessment: EXCELLENT — Active, well-maintained
```

**A risky dependency:**
```bash
$ repo_health some-old/lib --details
🔴 Health Score: 23/100
Last commit: 3 years ago ⚠️
License: None ❌
Open issues: 47 (0 closed recently)
Assessment: POOR — Likely abandoned
```

## Installation

```bash
# Copy the script (single file, zero deps)
curl -o repo_health https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/tools/repo_health.py
chmod +x repo_health

# Or use it directly
python3 repo_health.py owner/repo
```

## The Algorithm

The 0-100 score weighs multiple factors:

- **Activity (40%)**: Recent commits, PRs, issues closed
- **Community (30%)**: Stars, forks, watchers (social proof)
- **Maintenance (20%)**: Time since last commit, issue response
- **Legal (10%)**: Presence of LICENSE file

This isn't just star-counting. A repo with 10K stars but no commits in 2 years scores lower than a repo with 500 stars and weekly commits.

## When to Use This

**Before adding ANY dependency:**
- New npm/pip/cargo packages
- Forking a starter template
- Evaluating SaaS alternatives with open-source options
- Contributing to a project (check if PRs get merged)

**In CI/CD pipelines:**
```bash
# Fail build if dependency health < 60
repo_health owner/dependency --json | jq '.health_score' | xargs -I {} test {} -ge 60
```

## Beyond the Tool

`repo_health` is quick triage. For production dependencies, also consider:

1. **Security scanning**: Use Snyk, Dependabot, or GitHub Security Advisories
2. **Code review**: Actually read critical parts of the code
3. **Test coverage**: Does the project have tests? Do they pass?
4. **Documentation**: Will you be able to debug issues?

## The Code

The tool is ~150 lines of Python using only stdlib. No API key needed—it uses GitHub's public API with intelligent caching headers.

```python
# Core health calculation
def calculate_health(data: dict) -> int:
    score = 0
    
    # Activity scoring
    if data['pushed_at']:
        days = days_since(data['pushed_at'])
        if days < 7: score += 25
        elif days < 30: score += 20
        elif days < 90: score += 10
    
    # Community scoring  
    score += min(data['stargazers_count'] / 1000, 20)  # Cap at 20 pts
    score += min(data['forks_count'] / 500, 10)
    
    # Maintenance
    if not data['archived']: score += 15
    if data['open_issues_count'] < 50: score += 10
    
    # Legal
    if data.get('license'): score += 10
    
    return min(int(score), 100)
```

## Get It Free

`repo_health` is part of the [PD Researcher toolkit](https://github.com/barrowryan89-cloud/pd-researcher)—54 free CLI tools for developers.

Each tool solves one specific pain point. No bloat. No dependencies. Just works.

---

**Next up**: Check out [`ssl_cert`](./ssl-cert-checker) for TLS diagnostics or [`dns_probe`](./dns-probe) for DNS troubleshooting.

*Built with ♥ by [Plausible Deniability](https://10links.blue)*
