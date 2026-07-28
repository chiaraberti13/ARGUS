<div align="center">

# 👻 GhostTrack — Edizione Migliorata

**Un toolkit OSINT e di raccolta informazioni moderno, veloce e multipiattaforma**
*Geolocalizzazione IP · Analisi numeri di telefono · Ricerca username (50+ siti) · OSINT email*

[🇬🇧 English](README.md) · 🇮🇹 Italiano

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](.github/workflows/ci.yml)
[![Licenza: MIT](https://img.shields.io/badge/Licenza-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Piattaforme](https://img.shields.io/badge/piattaforme-Windows%20%7C%20Ubuntu%20%7C%20macOS-lightgrey)](#-installazione)

</div>

> ⚖️ **Solo per ricerca di sicurezza autorizzata, formazione OSINT e scopi educativi.**
> Sei l'unico responsabile di un uso legale ed etico dello strumento.
> Leggi [docs/DISCLAIMER.md](docs/DISCLAIMER.md).

---

## ✨ Cosa è stato migliorato rispetto all'originale

Questa è una riscrittura completa del classico [GhostTrack](https://github.com/HunxByts/GhostTrack): ne mantiene lo spirito potenziando quasi tutto.

| Ambito | Originale | Edizione Migliorata |
|--------|-----------|---------------------|
| **Architettura** | Script unico | Pacchetto Python pulito e testato (moduli, config, export) |
| **Ricerca username** | ~24 siti, sequenziale | **50+ siti, in parallelo** (thread pool) — secondi, non minuti |
| **Rilevamento** | Solo HTTP 200 | Stato HTTP **+ analisi del testo** per ridurre i falsi positivi |
| **Geolocalizzazione IP** | 1 provider (HTTP) | **2 provider con HTTPS + failover** e retry automatici |
| **Telefono** | Info di base | Validità, tipo di linea, operatore, regione, fusi orari, 4 formati |
| **Nuovi moduli** | — | **OSINT email**, **"il mio IP pubblico"** con geolocalizzazione |
| **Output** | Testo semplice | **Tabelle colorate** + barre di avanzamento (fallback testuale) |
| **Report** | Nessuno | Esportazione in **JSON / CSV / HTML** |
| **Interfaccia** | Solo menu | Menu interattivo **+ comandi CLI per scripting** |
| **Configurazione** | Fissa nel codice | File + variabili d'ambiente + flag (timeout, worker, UA, SSL…) |
| **Installazione** | Manuale (Linux/Termux) | **Installazione automatica con un comando su Windows, Ubuntu e macOS** + Docker |
| **Qualità** | — | Test unitari, lint ruff, CI GitHub Actions su 3 sistemi operativi |

---

## 🚀 Avvio rapido

### Installazione con un solo comando

**Ubuntu / Debian / macOS**
```bash
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
./scripts/install.sh          # aggiungi --with-dns per un OSINT email migliore
ghosttrack                    # avvia il menu interattivo
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
ghosttrack
```

L'installer rileva automaticamente il sistema operativo, installa Python se
necessario, crea un ambiente virtuale isolato, installa tutto e aggiunge il
comando `ghosttrack` al PATH. 👉 Guida completa passo-passo: **[docs/INSTALL.it.md](docs/INSTALL.it.md)**.

### Docker (senza Python installato in locale)
```bash
docker build -t ghosttrack .
docker run --rm -it ghosttrack                 # menu interattivo
docker run --rm ghosttrack ip 8.8.8.8          # comando singolo
```

---

## 🎯 Funzionalità e utilizzo

Avvia il **menu interattivo**:
```bash
ghosttrack
```

Oppure usalo **direttamente da riga di comando** (ideale per lo scripting):

```bash
# Geolocalizzazione IP (con failover + HTTPS)
ghosttrack ip 8.8.8.8

# Analisi numero di telefono
ghosttrack phone "+390212345678"
ghosttrack phone "02 1234 5678" --region IT

# Username su 50+ piattaforme (in parallelo)
ghosttrack username torvalds

# OSINT email passivo (sintassi, MX, Gravatar)
ghosttrack email qualcuno@example.com

# Il tuo IP pubblico + geolocalizzazione
ghosttrack myip

# Salva un report in qualsiasi esecuzione:
ghosttrack username torvalds --export html
ghosttrack ip 1.1.1.1 --export json
```

Riferimento completo dei comandi con tutti i flag: **[docs/USAGE.md](docs/USAGE.md)**.

### Report
Ogni ricerca può essere esportata in **JSON**, **CSV** o in un report **HTML**
autonomo (tema scuro e link cliccabili). I report vengono salvati per default
in `~/ghosttrack-reports/` (configurabile).

---

## ⚙️ Configurazione

Le impostazioni vengono risolte in quest'ordine: **flag CLI → variabili d'ambiente → file di config → valori predefiniti**.

| Impostazione | Flag | Variabile d'ambiente | Default |
|--------------|------|----------------------|---------|
| Timeout richiesta (s) | `--timeout` | `GHOSTTRACK_TIMEOUT` | `8.0` |
| Worker concorrenti | `--workers` | `GHOSTTRACK_MAX_WORKERS` | `20` |
| Retry | — | `GHOSTTRACK_RETRIES` | `2` |
| Cartella di output | — | `GHOSTTRACK_OUTPUT_DIR` | `~/ghosttrack-reports` |
| User-Agent | — | `GHOSTTRACK_USER_AGENT` | UA GhostTrack |
| Disattiva verifica SSL | — | `GHOSTTRACK_NO_VERIFY_SSL=1` | (verifica attiva) |

Crea un file di configurazione modificabile:
```bash
ghosttrack config --init      # crea ~/.config/ghosttrack/config.json
ghosttrack config --show      # mostra le impostazioni correnti
```

---

## 🗂️ Struttura del progetto

```
GhostTrack/
├── ghosttrack/               # il pacchetto Python
│   ├── cli.py                # menu + comandi CLI
│   ├── config.py             # configurazione a livelli
│   ├── ui.py                 # UI colorata con fallback testuale
│   ├── exporters.py          # report JSON / CSV / HTML
│   └── modules/              # ip, phone, username, email, myip
├── data/sites.json           # 50+ siti per username (facile da estendere)
├── scripts/                  # install.sh · install.ps1 · run.sh · run.bat
├── docs/                     # INSTALL / USAGE / DISCLAIMER (EN + IT)
├── tests/                    # test unitari offline
├── Dockerfile · Makefile · pyproject.toml
└── .github/workflows/ci.yml  # CI su Ubuntu, macOS, Windows
```

Vuoi aggiungere un sito alla ricerca username? Basta aggiungere una voce a
[`data/sites.json`](data/sites.json) — nessuna modifica al codice.

---

## 🧪 Sviluppo

```bash
make venv     # crea .venv e installa con gli extra di sviluppo
make test     # esegue i test offline
make lint     # ruff
make run      # avvia il menu
make docker   # costruisce l'immagine
```

---

## 🙏 Crediti e licenza

- Ispirato all'originale **GhostTrack** di [HunxByts](https://github.com/HunxByts).
- Distribuito con **[Licenza MIT](LICENSE)**.

## ⚠️ Uso legale ed etico

Questo progetto interroga esclusivamente informazioni e servizi **pubblicamente
disponibili**. Usalo solo su obiettivi di tua proprietà o per cui hai
un'autorizzazione esplicita. Leggi il **[disclaimer completo](docs/DISCLAIMER.md)**
prima dell'uso.
