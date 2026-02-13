# 35 Free Python CLI Tools That Saved Me 100+ Hours (Zero Dependencies)

*A curated collection of single-file scripts for developers who want results without the bloat*

---

## Why I Built These

After years of installing npm packages with 500 dependencies just to convert a JSON file, I got tired. Every tool seemed to require a full ecosystem. So I built 35 Python CLI tools that do one thing well — with **zero external dependencies**.

Just copy, paste, and run.

---

## The Complete Toolkit (Organized by Use Case)

### 🌐 Web & Content Tools

| Tool | What It Does | Command |
|------|--------------|---------|
| **HTML Cleaner** | Strip ads/scripts, convert to Markdown | `python3 html_cleaner_free.py <url>` |
| **URL Checker** | Check site status, response times | `python3 url_checker_free.py <url>` |
| **URL Shortener** | Shorten URLs via is.gd API | `python3 url_shortener_free.py <url>` |
| **Markdown → HTML** | Convert .md to styled HTML | `python3 markdown_to_html_free.py input.md` |
| **Link Extractor** | Pull all links from a webpage | `python3 link_extractor_free.py <url>` |

### 📊 Data Processing

| Tool | What It Does | Command |
|------|--------------|---------|
| **JSON Formatter** | Pretty print + validate JSON | `python3 json_formatter_free.py data.json` |
| **CSV Processor** | Sort, filter, convert CSV files | `python3 csv_processor_free.py data.csv` |
| **CSV → JSON** | Convert between formats | `python3 csv_to_json_free.py data.csv` |
| **JSON → CSV** | Flatten JSON to spreadsheet | `python3 json_to_csv_free.py data.json` |
| **HTML Table Gen** | CSV → styled HTML tables | `python3 html_table_generator_free.py data.csv` |
| **Text Summarizer** | Extractive summary of articles | `python3 text_summarizer_free.py article.txt` |

### 🔐 Security & Encoding

| Tool | What It Does | Command |
|------|--------------|---------|
| **Password Generator** | Secure passwords + entropy analysis | `python3 password_gen_free.py 20` |
| **Base64 Tool** | Encode/decode text and files | `python3 base64_tool_free.py encode "text"` |
| **Hash Generator** | MD5, SHA1, SHA256, SHA512 | `python3 hash_generator_free.py -f file.txt` |
| **JWT Decoder** | Decode JWT tokens (no verify) | `python3 jwt_decoder_free.py <token>` |
| **QR Code Gen** | Generate QR codes from text/URLs | `python3 qr_generator_free.py "Hello"` |

### 💻 Developer Utilities

| Tool | What It Does | Command |
|------|--------------|---------|
| **Timestamp Converter** | Unix ↔ Human-readable dates | `python3 timestamp_converter_free.py 1707772800` |
| **UUID Generator** | Cryptographically strong UUIDs | `python3 uuid_generator_free.py 5` |
| **Color Converter** | HEX ↔ RGB ↔ HSL | `python3 color_converter_free.py #FF5733` |
| **Regex Tester** | Test patterns against text | `python3 regex_tester_free.py "\\d+" text.txt` |
| **Diff Tool** | Compare two text files | `python3 diff_tool_free.py file1.txt file2.txt` |
| **Git Analyzer** | Repo stats, commits, contributors | `python3 git_analyzer_free.py` |
| **Port Scanner** | Check open ports on hosts | `python3 port_scanner_free.py example.com` |
| **HTTP Server** | Static file server with upload | `python3 http_server_free.py 8080` |

### 📝 Text & File Processing

| Tool | What It Does | Command |
|------|--------------|---------|
| **File Organizer** | Sort files by date/type | `python3 file_organizer_free.py ./downloads` |
| **Duplicate Finder** | Find duplicate files by hash | `python3 duplicate_finder_free.py ./folder` |
| **File Rename** | Bulk rename with patterns | `python3 file_renamer_free.py "*.txt"` |
| **Line Counter** | Count lines in code projects | `python3 line_counter_free.py ./src` |
| **Text Case Converter** | camelCase, snake_case, etc. | `python3 text_case_converter_free.py "hello world"` |
| **Word Counter** | Count words, chars, reading time | `python3 word_counter_free.py article.txt` |
| **Lorem Ipsum Gen** | Generate placeholder text | `python3 lorem_ipsum_free.py 5 paragraphs` |

### 🖼️ Image & Media

| Tool | What It Does | Command |
|------|--------------|---------|
| **Image Resizer** | Batch resize images | `python3 image_resizer_free.py ./photos 800x600` |
| **Screenshot Tool** | Capture screen regions | `python3 screenshot_tool_free.py` |

### 🧮 Math & Calculation

| Tool | What It Does | Command |
|------|--------------|---------|
| **Unit Converter** | Length, weight, temp, more | `python3 unit_converter_free.py 100 km to miles` |
| **Calculator** | Advanced math with history | `python3 calculator_free.py "sin(45) + sqrt(16)"` |

### 🖥️ System Info

| Tool | What It Does | Command |
|------|--------------|---------|
| **System Info** | OS, CPU, memory, disk usage | `python3 system_info_free.py` |
| **Process Monitor** | Watch running processes | `python3 process_monitor_free.py` |

---

## How to Get Them

All 35 tools are free, open source, and ready to use:

```bash
# Clone the repo
git clone https://github.com/barrowryan89-cloud/pd-researcher.git

# Or download individual tools
curl -O https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/tools/file_name_free.py
```

**Browse the full collection:** https://barrowryan89-cloud.github.io/pd-researcher/

---

## Why Zero Dependencies Matter

1. **No install hell** — No `node_modules` folders eating your disk
2. **No version conflicts** — Python 3.6+ is all you need
3. **Auditability** — Read the whole script in 30 seconds
4. **Portability** — Works on any system with Python
5. **Longevity** — These will still run in 2030

---

## My Top 5 Most-Used

1. **HTML Cleaner** — Daily use for research articles
2. **JSON Formatter** — Debugging APIs constantly
3. **Password Generator** — New credentials weekly
4. **Timestamp Converter** — Working across timezones
5. **File Organizer** — Downloads folder gets chaotic

---

## What's Next

I'm adding 2-3 new tools weekly. Current backlog:
- CSV → SQL converter
- Website archiver
- Git commit message generator
- API response mocking tool

**Star the repo** to get notified of new releases.

---

## License

All tools are MIT licensed. Use them, fork them, modify them — no attribution required.

---

*Built by a developer who was tired of dependency trees. For developers who value simplicity.*

**Star on GitHub →** https://github.com/barrowryan89-cloud/pd-researcher
