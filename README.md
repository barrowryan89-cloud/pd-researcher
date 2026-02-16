# ⚡️ 59 Free CLI Tools — Zero Dependencies, MIT Licensed

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tools](https://img.shields.io/badge/tools-59-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Stop writing "quick scripts" that take 2 hours. Start shipping in 10 seconds.**

This repository contains **59 battle-tested, single-file CLI tools**. **Zero dependencies.** Just copy, paste, and run. Save hours every week.

## 🎯 TL;DR
- 🧰 **59 single-purpose CLI tools** covering data, security, networking, monitoring, and productivity
- ⚙️ **Zero dependencies** — every script is pure Python stdlib, readable in under a minute
- ⚡ **Instant start** — `curl` any script, or grab the full ZIP / Vercel mirror if GitHub is throttled
- 🕵️ **Privacy-first** — everything runs locally, no telemetry, no API keys required
- 🆓 **MIT licensed** — use at work, redistribute in client stacks, or fork to customize
- 🧪 **Live demos** — Try the HTML converter + summarizer in-browser before downloading



## 🧭 Distribution Sprint — Status
We're running a focused Distribution Sprint to get these 59 tools in front of developers and teams. Status updates:

- Show HN: Scheduled (see content/SHOW_HN_POST_NOW.md)
- Product Hunt: Launch kit prepared (content/product_hunt_launch_kit.md)
- Top directories: Dev.to, Indie Hackers, AlternativeTo, StackShare queued

| Track | Status | Latest Move (Feb 15) | Next Action |
|-------|--------|----------------------|-------------|
| **Repo Polish** | ✅ Live | README hero + landing page copy cleaned; new scoreboard added for volunteers | Swap in fresh star-history graphic after Product Hunt preview |
| **Content** | 🟡 Queued | New X/LinkedIn revenue thread drafted in `content/social_drafts.md` | Ryan: Review + post alongside Show HN recap |
| **SEO / Landing** | ✅ Optimized | Index meta + structured data refreshed; mirror + ZIP links verified | Add spotlight testimonials once first directory approvals land |
| **Directories** | 🟠 In Flight | AlternativeTo, SaaSHub, StackShare packets sitting in `content/directory_form_prefills.md` | Submit Tier 1 targets + log proof in `content/directory_status_board.md` |
| **Affiliates** | 🟡 Prep | Tier-1 packets (DigitalOcean, 1Password, Sentry, JetBrains) staged in `content/affiliate_application_tracker.md` | Attach Vercel analytics screenshot + send applications |

Quick actions for contributors:
- Use the Vercel mirror (https://workspace-ivory-one.vercel.app) + direct ZIP in every submission
- Copy replies from content/show_hn_response_bank.md for fast moderator responses
- Report every submission in content/directory_status_board.md

## 🔗 Quick Links
- **Landing Page + Tool Directory:** https://workspace-ivory-one.vercel.app
- **Direct Download (ZIP, 1.2 MB):** https://workspace-ivory-one.vercel.app/pd-researcher.zip
- **Live Browser Tools:** https://workspace-ivory-one.vercel.app/html-converter.html & https://workspace-ivory-one.vercel.app/text-summarizer.html

## 🚀 Quick Start

Get any tool instantly:

```bash
# Download and run any tool directly (e.g., JSON Formatter)
curl -O https://workspace-ivory-one.vercel.app/tools/json_formatter_free.py
python3 json_formatter_free.py

# Or clone the full suite
git clone https://github.com/barrowryan89-cloud/pd-researcher.git
cd pd-researcher/tools
python3 password_gen_free.py
```

## ✨ The Tools (59 Total)

| Category | Count | Tools |
|----------|-------|-------|
| **Security** | 6 | password-gen, jwt-decoder, hash-generator, passgen, pwgen, hashgen |
| **Network** | 8 | port-scanner, ip-info, url-checker, dns-tool, http-request, webhook-tester, portprobe, portscan |
| **Data/Conversion** | 18 | json-formatter, csv-formatter, html-cleaner, base64-tool, markdown-to-html, color-converter, uuid-generator, timestamp-converter, unit-converter, sql-formatter, csv-processor, csv-tool, html-formatter, html-table-generator, html-entity, base64tool, qr-generator, qrgen |
| **Development** | 9 | git-analyzer, diff-tool, regex-tester, find-replace, line-counter, difftext, duplicate-finder, text-summarizer, regextest |
| **System** | 8 | system-info, process-monitor, memory-monitor, directory-size, file-splitter, backup-tool, dupesweeper, envvault |
| **Monitoring** | 6 | log-analyzer, cron-parser, cron-explainer, crontool, wallet-monitor, loglens |
| **Web/Utilities** | 4 | url-shortener, random-gen, css-formatter, word-freq |

### 🔥 Popular Tools

**Password Generator** — Secure passwords with entropy analysis
```bash
python3 tools/password_gen_free.py --length 32 --symbols
```

**JSON Formatter** — Pretty-print and validate JSON
```bash
cat data.json | python3 tools/json_formatter_free.py
```

**Port Scanner** — Check open ports with banner grabbing
```bash
python3 tools/port_scanner_free.py --host example.com --ports 80,443,8080
```

**Git Analyzer** — Repository health and contributor stats
```bash
python3 tools/git_analyzer_free.py /path/to/repo
```

**HTML Cleaner** — Extract article content from HTML
```bash
python3 tools/html_cleaner_free.py --url https://example.com/article
```

## 🚀 What Makes This Different

| Other Toolkits | This Repo |
|---------------|-----------|
| `pip install` + 50 dependencies | Zero dependencies, standard library only |
| Complex config files | Single file, read the code in 30 seconds |
| Framework lock-in | Drop into any project, any stack |
| Corporate licensing | MIT licensed, truly free |

**The rule:** If it needs `pip install`, it doesn't belong here.

## 💼 Professional Services

Need help integrating these tools or building custom automation?

- **Audits:** We map these tools to your stack (SOC 2, CI/CD, onboarding).
- **Customization:** We build bespoke zero-dependency tools for your team.
- **Contact:** DM [@barrowryan89](https://twitter.com/barrowryan89) or email `support@sandstreet.holdings`.

## 🤖 Bonus: The Propulsion Engine (How We Built This)

Curious how we built 59 tools in 48 hours? We didn't write them by hand.

Included in this repo is the **Propulsion Engine** prototype (`propulsion_daemon.sh` + `MASTER_AUTONOMOUS_PROMPT.md`). This is the exact agentic loop we used to:

1.  Identify missing tools
2.  Write the Python code (with zero dependencies)
3.  Self-correct errors
4.  Generate documentation

Check out `propulsion_daemon.sh` to see the bash-based agent orchestration logic. It's crude, but it works.

## 📁 Repository Structure

```
pd-researcher/
├── tools/              # 59 single-file CLI tools
│   ├── password_gen_free.py
│   ├── json_formatter_free.py
│   ├── port_scanner_free.py
│   └── ... (56 more)
├── propulsion_daemon.sh # The agentic loop script
├── MASTER_AUTONOMOUS_PROMPT.md # The system prompt for the engine
├── docs/               # Documentation
│   └── TOOLS.md       # Full tool reference
├── index.html         # Landing page source
└── README.md          # This file
```

## 🤝 Contributing

We love community tools!
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-tool`)
3. Follow the conventions:
   - Single Python file
   - Standard library only (no pip installs)
   - Include `--help` flag
   - MIT license header
4. Commit your changes
5. Push to the branch
6. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🔗 Links

- **Landing Page**: https://workspace-ivory-one.vercel.app
- **Repository**: https://github.com/barrowryan89-cloud/pd-researcher
- **Issues**: https://github.com/barrowryan89-cloud/pd-researcher/issues

---
*Built by developers, for developers.*
*Part of [Sand Street Holdings](https://github.com/barrowryan89-cloud)*
