# SMTP Server Validator

Test SMTP server connectivity, TLS support, and capabilities without sending actual emails. Perfect for debugging email configuration issues.

## Features

- 📧 **Connectivity Test** — Verify server is reachable
- 🔒 **TLS Detection** — Auto-detects STARTTLS support
- ✅ **Capability Check** — Tests EHLO/HELO responses
- 📊 **JSON Output** — For CI/CD pipelines
- ⚡ **Fast Timeout** — Configurable connection timeouts

## Usage

```bash
# Test Gmail SMTP
smtp_verify smtp.gmail.com 587

# Test with TLS on port 465
smtp_verify mail.example.com 465

# JSON output
smtp_verify localhost 25 --json

# Custom timeout
smtp_verify slow.server.com 587 --timeout 30
```

## Example Output

```
============================================================
📧 SMTP SERVER VALIDATOR
============================================================

📍 Target: smtp.gmail.com:587

✅ Status: REACHABLE

🔒 TLS Support:
   STARTTLS: Available
   TLS Version: TLSv1.3
   Cipher: TLS_AES_256_GCM_SHA384

📋 Server Info:
   Greeting: 220 smtp.gmail.com ESMTP
   Capabilities: STARTTLS, AUTH, SIZE, etc.

🕐 Response Time: 245ms
```

## Common Presets

| Provider | Host | Port |
|----------|------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |

## Install

```bash
curl -fsSL https://barrowryan89-cloud.github.io/pd-researcher/tools/smtp_verify.py > smtp_verify
chmod +x smtp_verify
./smtp_verify smtp.gmail.com 587
```

---

Part of [PD's Free Developer Tools](https://barrowryan89-cloud.github.io/pd-researcher/)
