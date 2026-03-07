# SSL Certificate Inspector

Quickly analyze SSL/TLS certificates for any hostname. Essential for DevOps, security audits, and debugging HTTPS issues.

## Features

- ✅ **Expiry Detection** — Color-coded warnings (green/yellow/red)  
- 🔒 **Certificate Details** — Subject, issuer, validity period  
- 🔐 **TLS Info** — Version, cipher suite, key size  
- 🌐 **SANs** — Subject Alternative Names  
- 📊 **JSON Output** — For CI/CD and automation  
- ⚠️ **Vulnerability Checks** — Weak ciphers, deprecated TLS

## Usage

```bash
# Basic check
ssl_cert google.com

# Custom port
ssl_cert api.example.com 8443

# Detailed output
ssl_cert site.com --verbose

# JSON for scripts
ssl_cert site.com --json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Valid certificate |
| 1 | Expired or invalid |
| 2 | Connection/verification error |

## Example Output

```
============================================================
🔒 SSL CERTIFICATE INSPECTOR
============================================================

📍 Target: google.com:443

✅ Status: VALID (65 days remaining)

📋 Subject:
   commonName: *.google.com

🏢 Issuer:
   countryName: US
   organizationName: Google Trust Services
   commonName: WR2

📅 Validity:
   Not Before: Jan 26 08:39:20 2026 GMT
   Not After:  Apr 20 08:39:19 2026 GMT

🔐 Connection:
   TLS Version: TLSv1.3
   Cipher:      TLS_AES_256_GCM_SHA384
   Key Size:    256 bits
```

## Install

```bash
curl -fsSL https://barrowryan89-cloud.github.io/pd-researcher/tools/ssl_cert.py > ssl_cert
chmod +x ssl_cert
./ssl_cert google.com
```

---

Part of [PD's Free Developer Tools](https://barrowryan89-cloud.github.io/pd-researcher/)
