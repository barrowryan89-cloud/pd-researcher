# Reddit r/Python Post — 98 Free CLI Tools

**Ready to Submit**

---

## Title

```
[OC] I built 98 free CLI tools in Python with zero dependencies
```

---

## Post Body

```
Over the last few months I built a collection of single-purpose 
CLI tools for common dev tasks. No pip install, no requirements.txt, 
just pure Python.

The collection includes:
✅ Data processing (HTML→Markdown, CSV↔JSON, text summarize)
✅ Security (password gen, hash, JWT decode, SSL cert check)
✅ Network (port scan, DNS lookup, API tester, URL checker)
✅ System (duplicate finder, disk usage, memory monitor)
✅ Dev tools (git stats, diff, regex tester, cron parser)

**Why zero dependencies?**

I've been burned too many times by package rot. A script I wrote 
2 years ago breaks because some dependency changed. These tools 
use only the Python standard library — they'll work in 5 years.

**Why single-file?**

Copy one file to any machine with Python. No venv, no Docker, 
no "works on my machine." Just copy and run.

**Quick examples:**

```bash
# Clean HTML to Markdown
python html_cleaner_free.py https://example.com/article

# Find duplicate photos
python dupesweeper_free.py ~/Pictures --delete-script

# Quick port scan
python port_scanner_free.py scanme.nmap.org --top-ports

# Check SSL certificate
python ssl_cert.py google.com --days-warning 30
```

All tools are:
• Single-file scripts
• Python 3.6+ compatible
• No external dependencies
• MIT licensed
• Pipe-friendly (Unix philosophy)

**GitHub:** https://github.com/barrowryan89-cloud/pd-researcher

Happy to take feature requests or contributions!
```

---

## Comment Responses

### If someone asks for a specific tool

```
Great idea! What's the use case? 

I try to follow Unix philosophy — one file, one job. If it fits 
that pattern, I'll add it.

Open an issue on GitHub with the details and I'll prioritize it.
```

### If someone criticizes "reinventing the wheel"

```
Fair critique! A few thoughts:

1. These aren't meant to replace professional tools (jq, ag, etc.)
2. They're for when you need something NOW without installation
3. The educational value — every tool is readable source
4. Package rot immunity — standard library only

If you have better tools installed, use those! These are for 
quick tasks on new machines, CI environments, or when you just 
need something that works without setup.
```

### If someone asks for a pip package

```
I intentionally avoided packaging. Here's why:

• pip install creates dependency hell
• These are meant to be copy-paste portable
• No version conflicts
• Easy to audit/modify for your needs

If you really want pip: `pip install git+https://...` works, 
but I recommend just copying the files you need.
```

---

## Cross-Posts

After posting to r/Python, cross-post to:
- r/commandline
- r/webdev (for HTML/URL tools)
- r/sysadmin (for system/network tools)
- r/coolgithubprojects

Wait 2-4 hours between posts to avoid spam detection.

---

## Engagement Tips

1. **Respond quickly** to first 5-10 comments (algorithm boost)
2. **Ask questions** — "What tool category would you add?"
3. **Share usage examples** — Real-world scenarios
4. **Be humble** — "These are simple tools for simple jobs"

---

## Timing

**Best:** Tuesday-Thursday, 9-11 AM EST  
**Avoid:** Weekends (lower engagement), Monday morning (competition)

---

**Status:** Ready to submit  
**Next Action:** Post to r/Python during peak hours
