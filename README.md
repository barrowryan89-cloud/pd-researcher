# PD_Researcher — 98 Free Developer Tools

> **98** command-line utilities that respect your time and privacy. Zero dependencies. Just Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)]()
[![Tool Count](https://img.shields.io/badge/tools-98-orange.svg)]()

---

## 🚀 Why 98 Tools?

I got tired of "npm install" breaking my scripts.  
I got tired of online tools selling my data.  
I got tired of bloated software for simple tasks.

So I built 98 single-purpose CLI tools. Each one:
- ✅ One file, one job
- ✅ Zero dependencies (no pip install required)
- ✅ Pure Python 3.6+
- ✅ MIT licensed

**They just work.** Today, tomorrow, in 5 years.

---

## 🎯 Quick Start

```bash
# Clone the repo
git clone https://github.com/barrowryan89-cloud/pd-researcher.git
cd pd-researcher

# Run any tool immediately
python tools/html_cleaner_free.py https://example.com
python tools/password_gen_free.py --length 32
python tools/qr_generator_free.py "https://yoursite.com"
```

**No installation. No dependencies. No signups.**

---

## 📦 The Tools (98 Total)

### Data Processing
| Tool | Purpose | Command |
|------|---------|---------|
| `html_cleaner_free.py` | Web → Markdown | `python html_cleaner_free.py <url>` |
| `text_summarizer_free.py` | Article summarization | `python text_summarizer_free.py <file>` |
| `json_formatter_free.py` | JSON formatting | `python json_formatter_free.py data.json` |
| `csv_processor_free.py` | CSV processing | `python csv_processor_free.py data.csv` |
| `csv_to_json.py` | CSV → JSON converter | `python csv_to_json.py data.csv` |
| `json_to_csv.py` | JSON → CSV converter | `python json_to_csv.py data.json` |
| `markdown_to_html_free.py` | Markdown → HTML | `python markdown_to_html_free.py file.md` |
| `html_table_generator_free.py` | CSV → HTML tables | `python html_table_generator_free.py data.csv` |

### Security & Crypto
| Tool | Purpose | Command |
|------|---------|---------|
| `password_gen_free.py` | Secure passwords | `python password_gen_free.py --length 32` |
| `password_analyzer.py` | Password strength check | `python password_analyzer.py -g` |
| `hash_generator_free.py` | File/string hashing | `python hash_generator_free.py file.txt` |
| `hashgen_free.py` | Universal hash generator | `python hashgen_free.py file.txt` |
| `base64_tool_free.py` | Encode/decode | `python base64_tool_free.py --encode file` |
| `jwt_decoder_free.py` | JWT token decoder | `python jwt_decoder_free.py <token>` |
| `ssl_cert.py` | SSL certificate inspector | `python ssl_cert.py google.com` |
| `wallet_monitor_free.py` | Crypto wallet tracking | `python wallet_monitor_free.py <address>` |

### Network & Web
| Tool | Purpose | Command |
|------|---------|---------|
| `url_checker_free.py` | Bulk URL validation | `python url_checker_free.py urls.txt` |
| `port_scanner_free.py` | Port scanning | `python port_scanner_free.py example.com` |
| `port_scan.py` | Fast TCP scanner | `python port_scan.py scanme.nmap.org --top` |
| `portscan_free.py` | Quick port checker | `python portscan_free.py host.com` |
| `ip_info_free.py` | IP address information | `python ip_info_free.py` |
| `dns_probe.py` | DNS record checker | `python dns_probe.py example.com --all` |
| `dnstool_free.py` | DNS lookup utility | `python dnstool_free.py example.com` |
| `http_request_free.py` | HTTP requests | `python http_request_free.py https://api.com` |
| `api_tester_free.py` | REST API testing | `python api_tester_free.py GET https://api.com` |
| `website_monitor_free.py` | Uptime monitoring | `python website_monitor_free.py check` |
| `url_shortener_free.py` | URL shortening | `python url_shortener_free.py <url>` |
| `url_parser_free.py` | URL parsing | `python url_parser_free.py parse "https://..."` |
| `smtp_verify.py` | SMTP server validator | `python smtp_verify.py smtp.gmail.com 587` |

### System & Files
| Tool | Purpose | Command |
|------|---------|---------|
| `duplicate_finder_free.py` | Find duplicate files | `python duplicate_finder_free.py /path` |
| `dupesweeper_free.py` | Advanced duplicate manager | `python dupesweeper_free.py ~/Downloads` |
| `directory_size_free.py` | Directory size analysis | `python directory_size_free.py /path` |
| `file_splitter_free.py` | Split large files | `python file_splitter_free.py file.zip` |
| `memory_monitor_free.py` | System memory monitoring | `python memory_monitor_free.py` |
| `process_monitor_free.py` | Process listing | `python process_monitor_free.py` |
| `system_info_free.py` | System diagnostics | `python system_info_free.py` |
| `line_counter_free.py` | Line/word counter | `python line_counter_free.py file.txt` |

### Development
| Tool | Purpose | Command |
|------|---------|---------|
| `git_analyzer_free.py` | Git repository stats | `python git_analyzer_free.py /path` |
| `repo_health.py` | GitHub repo analyzer | `python repo_health.py vercel/next.js` |
| `diff_tool_free.py` | File comparison | `python diff_tool_free.py file1.txt file2.txt` |
| `log_analyzer_free.py` | Log file analysis | `python log_analyzer_free.py access.log` |
| `loglens_free.py` | Advanced log parser | `python loglens_free.py app.log` |
| `regex_tester_free.py` | Regex testing | `python regex_tester_free.py "[a-z]+" "test"` |
| `cron_parser_free.py` | Cron expression parser | `python cron_parser_free.py "*/5 * * * *"` |
| `crontool_free.py` | Cron translator | `python crontool_free.py "0 9 * * 1"` |
| `find_replace_free.py` | Find/replace in files | `python find_replace_free.py pattern repl file` |
| `color_converter_free.py` | Color conversion | `python color_converter_free.py "#FF5733"` |
| `unit_converter_free.py` | Unit conversion | `python unit_converter_free.py 100 cm m` |
| `random_gen_free.py` | Random generator | `python random_gen_free.py password 20` |
| `uuid_generator_free.py` | UUID generation | `python uuid_generator_free.py --count 10` |
| `timestamp_converter_free.py` | Epoch/time conversion | `python timestamp_converter_free.py <timestamp>` |
| `timestamp_tool.py` | Unix timestamp tool | `python timestamp_tool.py now` |

### Utilities
| Tool | Purpose | Command |
|------|---------|---------|
| `qr_generator_free.py` | QR codes | `python qr_generator_free.py "https://yoursite.com"` |
| `backup_tool_free.py` | File backups | `python backup_tool_free.py /source /backup` |
| `css_formatter_free.py` | CSS formatting | `python css_formatter_free.py style.css` |
| `html_formatter_free.py` | HTML formatting | `python html_formatter_free.py page.html` |
| `html_extractor.py` | HTML text extractor | `python html_extractor.py --file page.html` |
| `htmlentity_free.py` | HTML entity encoder | `python htmlentity_free.py encode "text"` |
| `csv_formatter_free.py` | CSV formatting | `python csv_formatter_free.py data.csv` |
| `csv_converter_free.py` | CSV ↔ JSON | `python csv_converter_free.py data.csv` |
| `jsonfmt.py` | JSON formatter | `python jsonfmt.py data.json` |
| `csvtool_free.py` | CSV toolkit | `python csvtool_free.py data.csv` |
| `base64_tool.py` | Base64 utility | `python base64_tool.py encode "text"` |
| `url_encoder.py` | URL encode/decode | `python url_encoder.py encode "hello world"` |
| `hash_generator.py` | Hash & verify | `python hash_generator.py file doc.pdf` |
| `difftext_free.py` | Text diff | `python difftext_free.py a.txt b.txt` |
| `envvault_free.py` | Environment manager | `python envvault_free.py` |
| `webhook_tester_free.py` | Webhook testing | `python webhook_tester_free.py -p 8080` |
| `jwt_decode.py` | JWT decoder | `python jwt_decode.py <token>` |
| `cron_explainer_free.py` | Cron explainer | `python cron_explainer_free.py "0 0 * * *"` |
| `passgen_free.py` | Password generator | `python passgen_free.py` |
| `pwgen_free.py` | Secure pw generator | `python pwgen_free.py 20` |
| `api_probe.py` | API health check | `python api_probe.py https://api.com` |
| `http_probe.py` | HTTP probe | `python http_probe.py https://site.com` |
| `audit_lite.py` | Security audit | `python audit_lite.py` |
| `profile_polish.py` | Profile optimizer | `python profile_polish.py` |

---

## ✨ Why These Tools?

- **🔒 Privacy First** — All processing happens locally on your machine
- **📦 Zero Dependencies** — Pure Python, no pip installs required
- **⚡ Fast** — No network calls, no loading screens
- **🖥️ CLI Native** — Pipe-friendly, scriptable, automation-ready
- **🔧 Composable** — Chain tools together with Unix pipes
- **🕰️ Future-Proof** — No package rot. These work forever.

---

## 🆚 Free vs Paid

These tools are **free forever**. They solve 90% of common developer tasks.

Need more power? The **PD_Researcher Suite** adds:
- Batch processing (1000+ files)
- API integrations (OpenAI, Stripe, etc.)
- Research automation pipelines
- Custom tool generation

[Learn more →](https://barrowryan89-cloud.github.io/pd-researcher/)

---

## 🛡️ Security

- No network requests (unless explicitly fetching URLs)
- No telemetry or analytics
- No data collection
- Open source — audit the code yourself

---

## 📄 License

MIT License — use freely, modify freely, ship freely.

---

## 🌐 Web

**Landing Page:** https://barrowryan89-cloud.github.io/pd-researcher/  
**Full List:** See `tools/` directory

---

<p align="center">
  <i>Built by developers, for developers.</i><br>
  <i>98 tools. Zero dependencies. Infinite possibilities.</i>
</p>
