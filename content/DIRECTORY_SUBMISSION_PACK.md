# Directory Submission Pack — 59 CLI Tools

**Mission:** Submit to high-traffic developer directories for backlinks and traffic.

**⚠️ NOTE:** GitHub repo is currently suspended. Use the Vercel URL for submissions where possible, or wait for repo restoration.
**Vercel URL:** https://workspace-ivory-one.vercel.app

---

## 🎯 Priority Targets

### Tier 1: High Traffic, Easy Submit
| Directory | URL | Submit Time | Notes |
|-----------|-----|-------------|-------|
| **Dev.to** | dev.to | 10 min | Post as article with tool list |
| **Product Hunt** | producthunt.com | 30 min | Requires scheduling, maker comment ready |
| **Hacker News** | news.ycombinator.com | 5 min | Use SHOW_HN_POST_NOW.md |
| **GitHub Awesome Lists** | github.com | 15 min | BLOCKED until repo restored |
| **Reddit** | reddit.com | 10 min | r/commandline, r/webdev, r/programming |

### Tier 2: SEO Value
| Directory | URL | Submit Time | Notes |
|-----------|-----|-------------|-------|
| **AlternativeTo** | alternativeto.net | 15 min | Compare to paid tools |
| **Toolify.ai** | toolify.ai | 5 min | AI/dev tool directory |
| **DevPost** | devpost.com | 20 min | Showcase projects |
| **Mention** | mention.com | 10 min | Tool showcase |
| **LibHunt** | libhunt.com | 10 min | Python library ranking |

### Tier 3: Niche Communities
| Directory | URL | Submit Time | Notes |
|-----------|-----|-------------|-------|
| **Terminal Trove** | terminaltrove.com | 10 min | CLI-specific directory |
| **Awesome CLI** | github.com/alebcay/awesome-cli | 15 min | PR required |
| **Console.dev** | console.dev | 20 min | Curated dev tools |
| **StackShare** | stackshare.io | 15 min | Tool stack tracking |

---

## 📋 Dev.to Article Template

**Title:** 59 Free Python CLI Tools That Saved Me 100+ Hours

**Tags:** python, cli, developer-tools, productivity, open-source

**Body:**

I was tired of context switching. Every time I needed to validate JSON, convert a timestamp, or check a website's status, I left my terminal. Five minutes later, I'd forgotten what I was working on.

So I built 59 single-purpose CLI tools. Zero dependencies. Single files. MIT licensed.

## The Philosophy

**If it needs `pip install`, it doesn't belong here.**

Each tool is:
- One Python file (read it in 30 seconds)
- Zero external dependencies (stdlib only)
- Copy-paste-run (no config files)
- MIT licensed (truly free)

## The Tools

### Data Processing
- json_formatter_free.py — Pretty print + validate JSON
- csv_processor_free.py — Preview, filter, convert CSV
- hash_generator_free.py — MD5, SHA1, SHA256
- base64_tool_free.py — Encode/decode strings and files

### Security & Crypto
- password_gen_free.py — Secure passwords with entropy analysis
- jwt_decoder_free.py — Decode and validate JWT tokens
- ssl_cert.py — Certificate expiry and issuer info
- cert_checker_free.py — SSL/TLS chain validation

### Network & Web
- port_scanner_free.py — Check open ports with banner grab
- url_checker_free.py — Status codes + response times
- website_monitor_free.py — Uptime monitoring with CSV logs
- api_tester_free.py — HTTP client with saved requests
- webhook_tester_free.py — Local webhook receiver

### System & DevOps
- log_analyzer_free.py — Parse logs, count errors, extract IPs
- memory_monitor_free.py — Visual memory usage bars
- process_monitor_free.py — List processes with filtering
- directory_size_free.py — Find what's eating disk space
- duplicate_finder_free.py — Find dupes by hash

### Productivity
- diff_tool_free.py — Compare files line-by-line
- regex_tester_free.py — Test patterns with highlighting
- cron_parser_free.py — Explain cron in plain English
- timestamp_converter_free.py — Unix ↔ human readable
- html_cleaner_free.py — Web → clean Markdown
- text_summarizer_free.py — Extractive text summarization

## Quick Start

```bash
# Get the tools (zip download)
curl -O https://workspace-ivory-one.vercel.app/pd-researcher.zip
unzip pd-researcher.zip
cd tools
python3 json_formatter_free.py --help
```

## Why This Matters

Most "free" tools become subscription traps. These are actually free:
- No account required
- No API keys
- No data leaves your machine
- No vendor lock-in

## Try Them

🌐 Landing: https://workspace-ivory-one.vercel.app
📦 Download: https://workspace-ivory-one.vercel.app/pd-researcher.zip

---

## 📋 Product Hunt Launch Kit

**Title:** 59 Free CLI Tools for Developers

**Tagline:** Zero dependencies. Single files. MIT licensed.

**Description:**

I built 59 single-purpose CLI tools because I was tired of context switching. Every time I left my terminal to validate JSON or check a website, I lost 5 minutes of flow state.

Each tool is:
✅ One Python file (zero dependencies)
✅ Copy-paste-run (no pip install)
✅ MIT licensed (truly free)
✅ Works offline

From JSON formatting to port scanning to log analysis — these tools cover the daily friction points every developer faces.

**Topics:** Developer Tools, Productivity, Open Source, CLI

**Makers:** Ryan Barrow (@barrowryan89)

**Screenshots:**
- Hero: `assets/product-hunt-hero.png` (Brand new 59-tool graphic)
- Landing: `assets/landing-page-hero.png` (Full site preview)
- Tools: `assets/tool_shots/` (Terminal screenshots of port_scanner, etc.)

**Launch Time:** Tuesday 12:01 AM PT (optimal for Product Hunt)

**Maker Comment:**
> "I built these tools to solve my own workflow friction. The rule was simple: if it needs pip install, it doesn't belong here. Each tool is a single file you can read in 30 seconds. Hope they save you as much time as they've saved me!"

---

## 📋 Reddit Posts

### r/commandline
**Title:** [Showcase] 59 single-file CLI tools, zero dependencies

**Body:**

I built a collection of 59 Python CLI tools that follow one rule: zero dependencies.

Each tool is a single file using only stdlib. No pip install. No requirements.txt. Just copy, paste, run.

Tools include:
- JSON formatter/validator
- Port scanner with banner grab
- Log analyzer (count errors, extract IPs)
- Password generator with entropy analysis
- Webhook tester (local receiver)
- SSL cert inspector
- And 53 more...

Download: https://workspace-ivory-one.vercel.app/pd-researcher.zip
Landing: https://workspace-ivory-one.vercel.app

I use these daily to avoid context switching. The philosophy: if I have to leave my terminal, I've already lost.

Feedback welcome!

---

### r/webdev
**Title:** I built 59 free tools to stop leaving my terminal

**Body:**

Every context switch costs me 5 minutes of focus. Validating JSON on a website, checking if a server is up, converting timestamps — it all adds up.

So I built 59 single-purpose CLI tools:
- Zero dependencies (stdlib only)
- Single files (read in 30 seconds)
- MIT licensed (actually free)

Highlights for web devs:
- URL checker (status codes, redirects, response times)
- API tester (saved requests, history)
- Webhook tester (local receiver for Stripe/GitHub/Zapier)
- HTML cleaner (web → Markdown)
- JWT decoder (inspect tokens)

Quick start:
```bash
# Download zip
curl -O https://workspace-ivory-one.vercel.app/pd-researcher.zip
```

Full list: https://workspace-ivory-one.vercel.app

Would you use these? What other tools would you want?

---

### r/programming
**Title:** 59 Python CLI tools, zero dependencies, MIT licensed

**Body:**

I was spending 2 hours on "quick scripts" that should take 10 seconds. So I built 59 single-purpose CLI tools.

**The rules:**
1. One file per tool
2. Zero dependencies (stdlib only)
3. Copy-paste-run
4. MIT licensed

**Categories:**
- Data: JSON, CSV, hash, base64, UUID
- Security: Password gen, JWT decode, SSL cert
- Network: Port scan, URL check, API test, webhook
- System: Log analyze, memory monitor, process list
- Productivity: Diff, regex test, cron parse, timestamps

Link: https://workspace-ivory-one.vercel.app

All 59 tools are production-tested. I use them daily.

---

## 📋 GitHub Awesome List Submissions

### Target Lists:
1. https://github.com/alebcay/awesome-cli — General CLI tools
2. https://github.com/agarrharr/awesome-cli-apps — CLI applications
3. https://github.com/vinta/awesome-python — Python resources
4. https://github.com/trinib/awesome-python — Python tools

### PR Template:
```
Add PD_Researcher — 59 single-file CLI tools

59 Python CLI tools with zero dependencies. MIT licensed.

Categories: Data processing, security, networking, system tools, productivity.

Repo: https://github.com/barrowryan89-cloud/pd-researcher (Check if accessible)
```

---

## ✅ SUBMISSION CHECKLIST

### Week 1 (Immediate)
- [ ] Dev.to article published
- [ ] Hacker News Show HN posted
- [ ] Reddit r/commandline
- [ ] Reddit r/webdev
- [ ] Reddit r/programming

### Week 2 (Product Hunt)
- [ ] Product Hunt scheduled (Tuesday 12:01 AM PT)
- [ ] Screenshots prepared
- [ ] Maker comment drafted
- [ ] Social media promotion ready

### Week 3 (SEO Directories)
- [ ] AlternativeTo submission
- [ ] Toolify.ai submission
- [ ] Terminal Trove submission
- [ ] Console.dev application

### Week 4 (Awesome Lists)
- [ ] awesome-cli PR
- [ ] awesome-cli-apps PR
- [ ] awesome-python PR

---

**UTM Tracking Links:**
Use `utm_source=directory_name` for each submission to track traffic sources.

Example:
- Dev.to: `?utm_source=devto&utm_medium=article&utm_campaign=59tools`
- Product Hunt: `?utm_source=producthunt&utm_medium=launch&utm_campaign=59tools`
