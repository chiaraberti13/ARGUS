<div align="center">

# 👻 GhostTrack — Improved Edition

**A modern, fast, cross-platform OSINT & information-gathering toolkit**
*IP geolocation · Phone intelligence · Username hunting (50+ sites) · Email OSINT*

🇬🇧 English · [🇮🇹 Italiano](README.it.md)

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Ubuntu%20%7C%20macOS-lightgrey)](#-installation)

</div>

> ⚖️ **For authorized security research, OSINT training and education only.**
> You are solely responsible for using this tool legally and ethically.
> See [docs/DISCLAIMER.md](docs/DISCLAIMER.md).

---

## ✨ What's improved over the original

This is a ground-up rewrite of the classic [GhostTrack](https://github.com/HunxByts/GhostTrack), keeping the spirit while upgrading almost everything:

| Area | Original | Improved Edition |
|------|----------|------------------|
| **Architecture** | Single script | Clean, tested Python package (modules, config, exporters) |
| **Username search** | ~24 sites, sequential | **50+ sites, concurrent** (thread pool) — seconds, not minutes |
| **Detection** | HTTP 200 only | HTTP status **+ body-text matching** to cut false positives |
| **IP geolocation** | 1 provider (HTTP) | **2 providers with HTTPS + failover** and retries |
| **Phone** | Basic info | Validity, line type, carrier, region, timezones, 4 formats |
| **New modules** | — | **Email OSINT**, **"my public IP"** with geolocation |
| **Output** | Plain text | **Rich colored tables** + progress bars (graceful plain fallback) |
| **Reports** | None | Export to **JSON / CSV / HTML** |
| **Interface** | Menu only | Interactive menu **+ scriptable CLI subcommands** |
| **Config** | Hard-coded | File + env vars + flags (timeout, workers, UA, SSL…) |
| **Install** | Manual (Linux/Termux) | **One-command auto-install for Windows, Ubuntu & macOS** + Docker |
| **Quality** | — | Unit tests, ruff lint, GitHub Actions CI on 3 OSes |

---

## 🚀 Quick start

### One-command install

**Ubuntu / Debian / macOS**
```bash
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
./scripts/install.sh          # add --with-dns for better email OSINT
ghosttrack                    # launch the interactive menu
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
ghosttrack
```

The installer auto-detects your OS, installs Python if needed, creates an
isolated virtual environment, installs everything, and adds a `ghosttrack`
command to your PATH. 👉 Full step-by-step guide: **[docs/INSTALL.md](docs/INSTALL.md)**.

### Docker (no local Python needed)
```bash
docker build -t ghosttrack .
docker run --rm -it ghosttrack                 # interactive menu
docker run --rm ghosttrack ip 8.8.8.8          # one-off command
```

---

## 🎯 Features & usage

Launch the **interactive menu**:
```bash
ghosttrack
```

Or use it **directly from the command line** (great for scripting):

```bash
# IP geolocation (with failover + HTTPS)
ghosttrack ip 8.8.8.8

# Phone number intelligence
ghosttrack phone "+14155552671"
ghosttrack phone "02 1234 5678" --region IT

# Username across 50+ platforms (concurrent)
ghosttrack username torvalds

# Passive email OSINT (syntax, MX, Gravatar)
ghosttrack email someone@example.com

# Your own public IP + geolocation
ghosttrack myip

# Save a report in any run:
ghosttrack username torvalds --export html
ghosttrack ip 1.1.1.1 --export json
```

Full command reference with every flag: **[docs/USAGE.md](docs/USAGE.md)**.

### Reports
Every lookup can be exported to **JSON**, **CSV** or a self-contained **HTML**
report (with a dark theme and clickable links). Reports are written to
`~/ghosttrack-reports/` by default (configurable).

---

## ⚙️ Configuration

Settings are resolved in this order: **CLI flags → environment variables → config file → defaults**.

| Setting | Flag | Env var | Default |
|---------|------|---------|---------|
| Request timeout (s) | `--timeout` | `GHOSTTRACK_TIMEOUT` | `8.0` |
| Concurrent workers | `--workers` | `GHOSTTRACK_MAX_WORKERS` | `20` |
| Retries | — | `GHOSTTRACK_RETRIES` | `2` |
| Output directory | — | `GHOSTTRACK_OUTPUT_DIR` | `~/ghosttrack-reports` |
| User-Agent | — | `GHOSTTRACK_USER_AGENT` | GhostTrack UA |
| Disable SSL verify | — | `GHOSTTRACK_NO_VERIFY_SSL=1` | (verify on) |

Write a config file you can edit:
```bash
ghosttrack config --init      # creates ~/.config/ghosttrack/config.json
ghosttrack config --show      # print current settings
```

---

## 🗂️ Project structure

```
GhostTrack/
├── ghosttrack/               # the Python package
│   ├── cli.py                # menu + CLI subcommands
│   ├── config.py             # layered configuration
│   ├── ui.py                 # rich UI with plain fallback
│   ├── exporters.py          # JSON / CSV / HTML reports
│   └── modules/              # ip, phone, username, email, myip
├── data/sites.json           # 50+ username targets (easy to extend)
├── scripts/                  # install.sh · install.ps1 · run.sh · run.bat
├── docs/                     # INSTALL / USAGE / DISCLAIMER (EN + IT)
├── tests/                    # offline unit tests
├── Dockerfile · Makefile · pyproject.toml
└── .github/workflows/ci.yml  # CI on Ubuntu, macOS, Windows
```

Want to add a site to the username hunter? Just add an entry to
[`data/sites.json`](data/sites.json) — no code changes needed.

---

## 🧪 Development

```bash
make venv     # create .venv and install with dev extras
make test     # run the offline test suite
make lint     # ruff
make run      # launch the menu
make docker   # build the image
```

---

## 🙏 Credits & license

- Inspired by the original **GhostTrack** by [HunxByts](https://github.com/HunxByts).
- Licensed under the **[MIT License](LICENSE)**.

## ⚠️ Legal & ethical use

This project only queries **publicly available** information and services.
Use it exclusively on targets you own or are explicitly authorized to
investigate. Read the full **[disclaimer](docs/DISCLAIMER.md)** before use.
