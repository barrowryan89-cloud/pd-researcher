# ⚡️ 59 Free CLI Tools — Zero Dependencies, MIT Licensed

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tools](https://img.shields.io/badge/tools-59-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Stop writing "quick scripts" that take 2 hours. Start shipping in 10 seconds.**

This repository contains **59 battle-tested, single-file CLI tools**. **Zero dependencies.** Just copy, paste, and run. Save hours every week.

## 🚀 What Makes This Different

| Other Toolkits | This Repo |
|---------------|-----------|
| `pip install` + 50 dependencies | Zero dependencies, standard library only |
| Complex config files | Single file, read the code in 30 seconds |
| Framework lock-in | Drop into any project, any stack |
| Corporate licensing | MIT licensed, truly free |

**The rule:** If it needs `pip install`, it doesn't belong here.

## 🚀 Quick Start

Get any tool instantly:

```bash
# Download and run any tool directly
curl -O https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/tools/json_formatter_free.py
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

## 📁 Repository Structure

```
pd-researcher/
├── tools/              # 59 single-file CLI tools
│   ├── password_gen_free.py
│   ├── json_formatter_free.py
│   ├── port_scanner_free.py
│   └── ... (56 more)
├── docs/               # Documentation
│   └── TOOLS.md       # Full tool reference
├── index.html         # Landing page
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

- **Landing Page**: https://workspace-mv9axwdi5-ryan-barrows-projects.vercel.app
- **Repository**: https://github.com/barrowryan89-cloud/pd-researcher
- **Issues**: https://github.com/barrowryan89-cloud/pd-researcher/issues

---
*Built by developers, for developers.*
*Part of [Sand Street Holdings](https://github.com/barrowryan89-cloud)*
