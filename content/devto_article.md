# 98 Free CLI Tools Every Developer Should Know

> A curated collection of zero-dependency Python tools for data processing, security, networking, and more.

---

## The Problem with Modern Developer Tools

We've all been there. You find a perfect CLI tool, install it with `npm install -g`, use it for a year, then come back to find it broken. Dependencies changed. Node versions conflicted. The maintainer abandoned it.

Or worse — you need a quick tool on a fresh machine. Cue 20 minutes of installing dependencies, fighting with package managers, and wrestling with version conflicts.

**What if tools just worked?**

---

## Introducing: Zero-Dependency CLI Tools

I spent the last few months building **98 single-purpose CLI tools** that share one philosophy:

- **One file, one job**
- **Zero dependencies** (Python standard library only)
- **MIT licensed** (use freely, modify freely)
- **Forever portable** (copy and run anywhere)

No `pip install`. No `requirements.txt`. No Docker. Just Python 3.6+.

---

## Tool Categories

### 📊 Data Processing (12 tools)

**HTML Cleaner** — Convert messy web articles to clean Markdown
```bash
python html_cleaner_free.py https://example.com/article
```

**JSON Formatter** — Pretty print with error detection
```bash
python json_formatter_free.py data.json
```

**CSV Processor** — Filter, preview, convert without Excel
```bash
python csv_processor_free.py data.csv --preview
```

**Text Summarizer** — Extract key points from articles
```bash
python text_summarizer_free.py article.txt --sentences 5
```

### 🔐 Security (8 tools)

**Password Generator** — Cryptographically secure with entropy analysis
```bash
python password_gen_free.py --length 32 --symbols
```

**Hash Generator** — MD5, SHA1, SHA256 for files and strings
```bash
python hash_generator_free.py file.txt --algorithm sha256
```

**JWT Decoder** — Inspect tokens, check expiration
```bash
python jwt_decoder_free.py "eyJhbGciOiJIUzI1NiJ9..."
```

**SSL Certificate Inspector** — Check expiry, issuer, vulnerabilities
```bash
python ssl_cert.py google.com --days-warning 30
```

### 🌐 Network (12 tools)

**Port Scanner** — Quick TCP scans without Nmap
```bash
python port_scanner_free.py scanme.nmap.org --top-ports
```

**DNS Lookup** — Records, reverse lookup, propagation check
```bash
python dns_probe.py example.com --all
```

**API Tester** — HTTP client with history and analysis
```bash
python api_tester_free.py GET https://api.github.com/user
```

**URL Checker** — Batch validate URLs with status codes
```bash
python url_checker_free.py urls.txt
```

### 💻 System (8 tools)

**Duplicate Finder** — Find duplicate files by hash
```bash
python dupesweeper_free.py ~/Downloads --script
```

**Directory Size** — What's eating your disk space?
```bash
python directory_size_free.py /var/log --human-readable
```

**Memory Monitor** — Visual memory usage with warnings
```bash
python memory_monitor_free.py --watch
```

**Log Analyzer** — Extract errors, IPs, patterns
```bash
python log_analyzer_free.py access.log --errors-only
```

### 🛠️ Developer Tools (15+ tools)

**Git Analyzer** — Repository stats and insights
```bash
python git_analyzer_free.py /path/to/repo
```

**Repo Health** — GitHub repository 0-100 health score
```bash
python repo_health.py vercel/next.js --details
```

**Diff Tool** — Compare files line-by-line
```bash
python diff_tool_free.py file1.txt file2.txt --color
```

**Regex Tester** — Pattern matching with groups
```bash
python regex_tester_free.py "[a-z]+" "test123" --groups
```

**Cron Parser** — Human-readable cron explanations
```bash
python cron_parser_free.py "*/5 * * * *"
# Output: Every 5 minutes
```

---

## Why Zero Dependencies?

### 1. Package Rot Immunity

Dependencies change. APIs break. Maintainers move on. Tools using only the standard library work forever.

### 2. Instant Portability

Copy one file to any machine with Python. No environment setup. No "works on my machine."

### 3. Easy to Audit

Every tool is <200 lines. Read and understand it in 5 minutes. No hidden surprises in dependency trees.

### 4. Unix Philosophy

Do one thing well. Pipe them together. Chain for complex workflows.

```bash
# Example: Download article, summarize, save
python html_cleaner_free.py https://example.com \
  | python text_summarizer_free.py --stdin > summary.txt
```

---

## Real-World Use Cases

### Scenario 1: Cleaning Up Photos

```bash
# Find duplicate photos across multiple folders
python dupesweeper_free.py ~/Pictures ~/Backup --delete-script

# Review script before running
./delete_duplicates.sh
```

### Scenario 2: API Debugging

```bash
# Test endpoint with timing
python api_tester_free.py POST https://api.com/data \
  --header "Authorization: Bearer $TOKEN" \
  --data '{"key":"value"}' \
  --timing
```

### Scenario 3: Log Analysis

```bash
# Extract all 5xx errors with IPs
python log_analyzer_free.py access.log --status 5xx --extract-ip \
  | sort | uniq -c | sort -rn
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/barrowryan89-cloud/pd-researcher.git
cd pd-researcher

# Run any tool immediately
python tools/html_cleaner_free.py https://example.com
```

That's it. No installation. No dependencies. Just works.

---

## The Full Collection

| Category | Tools | Use Case |
|----------|-------|----------|
| Data Processing | 12 | CSV, JSON, HTML, Markdown |
| Security | 8 | Passwords, hashing, SSL, JWT |
| Network | 12 | Scanning, DNS, API testing |
| System | 8 | Files, memory, processes, logs |
| Dev Tools | 15 | Git, diff, regex, cron |
| Utilities | 43 | Converters, generators, formatters |

**Total: 98 tools** — all free, all open source, all zero dependencies.

---

## Contributing

Found a bug? Want a new tool? Open an issue or PR on GitHub.

The criteria for new tools:
- Single-purpose
- Standard library only
- <200 lines
- Pipe-friendly

---

## Conclusion

Modern development doesn't have to mean modern complexity. Sometimes the best tool is a simple script that does one thing well.

These 98 tools are my answer to dependency hell. Use them, modify them, make them yours.

**[Get the tools on GitHub →](https://github.com/barrowryan89-cloud/pd-researcher)**

---

*Built with ❤️ by [Sand Street Holdings](https://sandstreet.holdings)*  
*MIT Licensed — use freely, modify freely, ship freely*

---

## Discussion

**What CLI tools do you wish had simpler alternatives?** Let me know in the comments!

---

*Originally published on [dev.to](https://dev.to)*
