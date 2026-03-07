# Show HN: I built 98 free CLI tools with zero dependencies

**Show HN Post — Ready to Submit**

---

## Title Options (Pick One)

**Primary:** Show HN: I built 98 free CLI tools with zero dependencies  
**Alternative:** Show HN: 98 single-file Python tools — no pip install required  
**Short:** Show HN: 98 CLI tools, zero dependencies

---

## Post Body

```
I got tired of "npm install" breaking my scripts every 6 months.

So I built 98 single-purpose CLI tools. Each one:
- One file, one job
- Zero dependencies (no pip install)
- Pure Python 3.6+
- MIT licensed

The tools cover:
• Data processing (HTML→Markdown, JSON, CSV)
• Security (password gen, hash, JWT, SSL)
• Network (port scan, DNS, API testing)
• System (dupe finder, disk usage, logs)
• Dev tools (git stats, diff, regex, cron)

Why zero dependencies?
Package rot killed too many of my scripts. These work today, 
tomorrow, in 5 years. Copy a file, run it, done.

Examples:
  python html_cleaner_free.py https://example.com
  python port_scanner_free.py scanme.nmap.org
  python dupesweeper_free.py ~/Downloads --script

GitHub: https://github.com/barrowryan89-cloud/pd-researcher

Happy to take feedback or tool requests!
```

---

## Comment Strategy

### If someone asks "Why not just use existing tools?"

```
Fair question! A few reasons:

1. Package rot — I've had scripts break because a dependency 
   dropped Python 2 support or changed an API. These don't.

2. Portability — Copy one file to any machine with Python. 
   No environment setup, no venv, no Docker.

3. Auditability — Every tool is <200 lines. You can read and 
   understand the whole thing in 5 minutes.

4. Composability — Pipe them together. They're designed for 
   Unix philosophy: do one thing well.

That said, if you have existing tools that work, keep using them! 
These are for when you want something that just works, forever.
```

### If someone says "98 is too many"

```
You're not supposed to use all 98! 

Think of it like a hardware store — you don't buy every tool, 
you grab the one you need for today's job.

The value is:
• When you need it, it's there
• No search/evaluate/install cycle
• It works immediately

I probably use 10-15 regularly. The rest are for edge cases.
```

### If someone asks about performance

```
These are Python scripts — not winning any speed contests.

But for the tasks they do (parse JSON, check URLs, format CSV), 
they're fast enough. The bottleneck is usually I/O, not CPU.

If you need to hash 10TB or scan 10k ports/second, reach for 
Rust/Go. For everyday dev tasks, these work great.
```

---

## Timing Strategy

**Best time to post:** Tuesday-Thursday, 8-10 AM PST  
**Why:** East Coast is at lunch, West Coast is starting work, Europe is online

**Backup times:**
- Monday 9 AM PST (week start energy)
- Friday 2 PM PST (weekend project browsing)

---

## Follow-up Comments (Post After 30 mins)

If initial traction is good, add:

```
Update: Since there's interest, here's a quick breakdown of 
most-used tools based on my own usage:

1. html_cleaner_free.py — Daily. Reading articles without ads.
2. dupesweeper_free.py — Weekly. Photo cleanup.
3. port_scanner_free.py — Debugging services.
4. json_formatter_free.py — API debugging.
5. password_gen_free.py — New account creation.

The pattern: quick tasks that don't need a full app.
```

---

## Success Metrics to Watch

| Metric | Good | Great |
|--------|------|-------|
| Upvotes | 100+ | 500+ |
| Comments | 30+ | 100+ |
| GitHub stars (24h) | 200+ | 1000+ |
| Traffic to landing page | 1000+ | 5000+ |

---

## Cross-Post Strategy

After HN post gains traction (~2-4 hours):
1. Post to r/Python (link to HN discussion)
2. Tweet with HN screenshot
3. Update PH launch to reference HN success

---

**Status:** Ready to submit  
**Next Action:** Copy post body, submit during peak hours
