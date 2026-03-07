# I built 55 free CLI tools for developers — here are the most useful ones

Hey r/devops,

I've been on a mission to build useful CLI tools that solve real developer pain points. No signup, no BS, just grab and use.

**Top picks for DevOps/SREs:**

### 1. `port_scan` — Fast port scanner
Async TCP scanner that checks 1000 ports in ~10 seconds. Great for quick network diagnostics.
```bash
port_scan api.example.com --range 1-1000
port_scan server.local --ports 22,80,443,3306 --json
```

### 2. `ssl_cert` — SSL certificate inspector
Shows expiry, issuer, cipher strength, SANs. Color-coded warnings for expiring certs.
```bash
ssl_cert api.mysite.com --verbose
ssl_cert site.com --json  # For CI/CD monitoring
```

### 3. `dns_probe` — DNS record checker
Health score + full record inspection (A, AAAA, MX, TXT, SPF, DMARC).
```bash
dns_probe google.com --all
dns_probe example.com --json
```

### 4. `smtp_verify` — SMTP validator
Diagnose email server issues without sending actual emails.
```bash
smtp_verify smtp.gmail.com 587
smtp_verify mail.company.com 25 --json
```

### 5. `repo_health` — GitHub repo analyzer
Quick due diligence before adopting dependencies. Health score 0-100.
```bash
repo_health vercel/next.js --details
repo_health some-random-lib --json
```

**All tools:**
- Single Python files (copy/paste or curl)
- No dependencies beyond Python 3.7+
- JSON output for automation
- MIT licensed

**Grab them:** github.com/barrowryan89-cloud/pd-researcher

What tools would you actually use? I'm taking requests.
