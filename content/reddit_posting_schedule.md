# Reddit Posting Schedule & Templates

**Status:** COPY-PASTE READY — Post after GitHub Pages fixed  
**Strategy:** Staggered posts across 4 subreddits over 2 weeks

---

## 📅 Posting Schedule

| Day | Subreddit | Time (ET) | Template | Expected |
|-----|-----------|-----------|----------|----------|
| Day 1 | r/commandline | 10 AM | Template 1 | 500-1,500 upvotes |
| Day 3 | r/webdev | 9 AM | Template 2 | 300-800 upvotes |
| Day 7 | r/python | 11 AM | Template 3 | 200-600 upvotes |
| Day 10 | r/programming | 9 AM | Template 4 | 400-1,200 upvotes |
| Day 14 | r/selfhosted | 2 PM | Template 5 | 150-400 upvotes |

**Why stagger?**
- Avoid looking like spam
- Learn from each post's feedback
- Build momentum across communities

---

## 📝 Template 1: r/commandline (Day 1)

**Title:**
```
I built 98 single-file CLI tools — zero dependencies, MIT licensed
```

**Body:**
```
Hey r/commandline,

I found myself rewriting the same scripts across projects, so I standardized them into a collection of 98 single-purpose CLI utilities.

**Design principles:**
- Single file per tool (easy to audit/modify)
- Zero dependencies beyond stdlib (just works™)
- MIT licensed (use however you want)
- POSIX-ish where possible

**Categories:**
- File/text processing (json, csv, diff, hash)
- System info (net, process, sys monitor)
- Security (password gen, file encrypt, cert check)
- DevOps (port scan, website monitor, log analyzer)
- Productivity (pomodoro, todo, timestamp)

**Most used (personally):**
1. `port_scanner_free.py` — quick port checks without nmap
2. `json_formatter_free.py` — pipe JSON, get formatted output
3. `password_gen_free.py` — generate secure passwords locally

Repo: https://github.com/barrowryan89-cloud/pd-researcher

Would love feedback from this community — any tools I'm missing? Any that could be improved?
```

**Why this works for r/commandline:**
- Technical details first (they care about implementation)
- Emphasizes single-file/zero-deps (core values of CLI culture)
- Asks for feedback (community loves to improve things)
- No self-promotion language

---

## 📝 Template 2: r/webdev (Day 3)

**Title:**
```
The $0 Dev Stack: 98 CLI tools that replaced my SaaS subscriptions
```

**Body:**
```
As a broke indie hacker, I couldn't justify $200+/month for developer tools. So I built my own.

**What I replaced:**
- JSON formatter (was: jsonlint.com) → `json_formatter_free.py`
- Password generator (was: LastPass generator) → `password_gen_free.py`
- Port checker (was: online-port-scanner.com) → `port_scanner_free.py`
- Cron parser (was: crontab.guru) → `cron_parser_free.py`
- URL shortener (was: bit.ly) → `url_shortener_free.py`

**The stack:**
- Language: Python 3 (stdlib only)
- Philosophy: Single file = single purpose
- License: MIT (fork and modify)
- Cost: $0 forever

**Caveats:**
- Not "enterprise grade" (yet)
- No GUI (terminal only)
- You host/maintain them

But for my workflow? Perfect. I own my tools, no subscription fatigue, and I can customize anything.

Full collection: https://github.com/barrowryan89-cloud/pd-researcher

Anyone else building their own tools instead of subscribing?
```

**Why this works for r/webdev:**
- Problem/solution narrative (relatable to indie devs)
- Specific "before/after" examples
- Honest about limitations (builds trust)
- Question at end encourages discussion

---

## 📝 Template 3: r/python (Day 7)

**Title:**
```
Show r/python: 98 CLI tools, all stdlib, no pip install required
```

**Body:**
```
I wanted to share a project I've been working on — a collection of 98 CLI utilities built entirely with Python's standard library.

**Why no external dependencies?**
- Copy to any system with Python and it works
- No version conflicts or broken installs
- Easy to audit (each tool is one file)
- Can run in restricted environments

**Tool examples:**
```python
# json_formatter_free.py
import json, sys
print(json.dumps(json.load(sys.stdin), indent=2))

# password_gen_free.py  
import secrets, string
print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)))
```

**Categories:**
- Data processing (json, csv, html, base64)
- Network (port scan, whois, dns, ip info)
- System (process monitor, directory size, file compare)
- Text (diff, word freq, find/replace, regex tester)

Each tool is independently useful — grab just what you need.

Repo: https://github.com/barrowryan89-cloud/pd-researcher

Feedback welcome! Especially interested in Pythonic improvements.
```

**Why this works for r/python:**
- Code samples (they love seeing actual Python)
- Emphasizes stdlib usage (point of pride for Python devs)
- Technical depth in explanation
- Specifically asks for Python feedback

---

## 📝 Template 4: r/programming (Day 10)

**Title:**
```
I built 98 CLI tools to solve my workflow friction — here is what I learned
```

**Body:**
```
**The problem:**
Every time I left my terminal to use an online tool (JSON formatter, timestamp converter, password generator), I lost flow state. Context switching kills productivity.

**The solution:**
98 single-purpose CLI tools that live in my terminal.

**What I learned:**

1. **Volume beats perfection.** I built fast, iterated later. The first version of each tool took 10-30 minutes. If it solved my problem, I shipped it.

2. **The "boring" tools get the most use.** My most-run script? A simple port killer. Saves 5 minutes of frustration every time. 5 min × 200 days = 16 hours saved/year.

3. **Zero dependencies = zero friction.** No pip install, no npm packages, no Docker. Just Python stdlib. Copy the file, run it, done.

4. **Single files are underrated.** Each tool is one file. Easy to audit, easy to modify, easy to share. No digging through src/ directories.

**The collection:**
https://github.com/barrowryan89-cloud/pd-researcher

Categories: Git workflows, DevOps, security, data processing, productivity

**Question for you:**
What workflow friction have you automated away with custom scripts?

Would love to hear what others have built for their own workflows.
```

**Why this works for r/programming:**
- Lesson-focused (they love learning from others)
- Quantified value (16 hours saved)
- Discusses methodology, not just output
- Ends with discussion question

---

## 📝 Template 5: r/selfhosted (Day 14)

**Title:**
```
Self-hosted CLI toolkit: 98 tools, no external dependencies, fully auditable
```

**Body:**
```
I wanted to share a project that aligns with self-hosting philosophy — a collection of 98 CLI tools that require no cloud services, no accounts, no subscriptions.

**Why this fits self-hosting:**
- ✅ No network calls (unless tool specifically needs it)
- ✅ No telemetry or tracking
- ✅ Single files = fully auditable in minutes
- ✅ Zero dependencies = no supply chain risks
- ✅ MIT licensed = truly yours

**Tools particularly useful for self-hosters:**
- `port_scanner_free.py` — check what ports are open
- `website_monitor_free.py` — monitor your services
- `cert_checker_free.py` — SSL cert validation
- `log_analyzer_free.py` — parse and analyze logs
- `sys_monitor_free.py` — system resource monitoring
- `file_encrypt_free.py` — local file encryption

**Running them:**
```bash
# Download just what you need
curl -O https://raw.githubusercontent.com/barrowryan89-cloud/pd-researcher/main/port_scanner_free.py
python3 port_scanner_free.py --help
```

**Repo:** https://github.com/barrowryan89-cloud/pd-researcher

Anyone else preferring local tools over web services? What are your go-to self-hosted utilities?
```

**Why this works for r/selfhosted:**
- Aligns with community values (privacy, control, auditability)
- Highlights tools relevant to their use case
- Emphasizes security benefits
- Asks about their stack

---

## 💬 Engagement Strategy

### First 2 Hours (Critical)
- Reply to every comment
- Upvote thoughtful responses
- Be humble and helpful
- Don't get defensive

### First 24 Hours
- Continue replying to questions
- Share additional context when asked
- Thank people for feedback
- Note suggestions for future tools

### Ongoing
- Check back daily for new comments
- Update post if you make improvements based on feedback
- Cross-link to other community discussions

---

## 🚨 What NOT To Do

❌ **Don't:** Post to all subreddits at once  
❌ **Don't:** Use the same title/body everywhere  
❌ **Don't:** Argue with critics  
❌ **Don't:** Delete posts if they don't perform  
❌ **Don't:** Ask for upvotes anywhere  
❌ **Don't:** Post if your account is <30 days old  

---

## ✅ Pre-Flight Checklist

- [ ] Reddit account >30 days old with some karma
- [ ] GitHub Pages 404 fixed
- [ ] Read each subreddit's rules
- [ ] Templates customized for each community
- [ ] Time blocked for engagement
- [ ] UTM links ready for tracking
- [ ] Thick skin ready (Reddit can be critical)

---

## 📊 Expected Results

| Subreddit | Est. Upvotes | Est. Comments | Est. Traffic |
|-----------|--------------|---------------|--------------|
| r/commandline | 500-1,500 | 100-300 | 800-2,000 |
| r/webdev | 300-800 | 50-150 | 500-1,200 |
| r/python | 200-600 | 80-200 | 400-1,000 |
| r/programming | 400-1,200 | 150-400 | 1,000-2,500 |
| r/selfhosted | 150-400 | 30-80 | 200-600 |
| **TOTAL** | **1,550-4,500** | **410-1,130** | **2,900-7,300** |

---

**Status:** READY TO POST  
**Blocker:** GitHub Pages 404 must be fixed  
**Next Action:** Start with r/commandline 3 days after GitHub Pages is live

---

*Created: 2026-02-14*
