<div align="center">

```
     _    ____   ____ _   _ ____
    / \  |  _ \ / ___| | | / ___|
   / _ \ | |_) | |  _| | | \___ \
  / ___ \|  _ <| |_| | |_| |___) |
 /_/   \_\_| \_\\____|\___/|____/
```

# Argus

**The all-seeing OSINT & reconnaissance toolkit**
*IP · Domain · DNS · Phone · Username · Email · Web · MAC — one fast, unified CLI*

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](.github/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Ubuntu%20%7C%20macOS-lightgrey)](#-installation)

**🇬🇧 [English](#-english) · 🇮🇹 [Italiano](#-italiano)**

</div>

> ⚖️ **For authorized security research, OSINT training and education only.**
> Argus only queries **publicly available** information. You are solely
> responsible for using it **lawfully and ethically** — read the full
> **[disclaimer](docs/DISCLAIMER.md)** before use.

---

<a name="-english"></a>
## 🇬🇧 English

### What is Argus?

**Argus is a command-line toolkit for OSINT (Open Source Intelligence)** —
the practice of gathering information from *public, freely accessible* sources.
It brings together the reconnaissance steps an analyst normally does across a
dozen separate websites and tools into **one fast, consistent interface**, and
performs every lookup **passively**: it only reads public data and never
attacks, logs into, or probes private systems.

Give Argus an identifier — an IP, a domain, a phone number, a username, an email,
a URL or a MAC address — and it enriches it with everything public sources know
about it, then presents the result in clean colored tables and can save a
JSON / CSV / HTML report.

**Who it's for and what it's used for:**
- 🛡️ **Security professionals** — the reconnaissance phase of an *authorized*
  penetration test or red-team engagement (map a target's infrastructure).
- 🔎 **Threat intelligence & incident response** — quickly enrich an indicator
  (IP, domain, hash of an email) seen in logs or an alert.
- 🕵️ **OSINT analysts & investigators** — build a subject's public digital
  footprint from data they have chosen to make public.
- 🙋 **Privacy-conscious individuals** — audit *your own* exposure: which sites
  show your username, what your public IP reveals, what a domain leaks.
- 🎓 **Students & educators** — a hands-on, well-documented way to learn how
  OSINT, DNS, WHOIS, HTTP and geolocation actually work.

### 🧰 Modules

| Command | What it does |
|---------|--------------|
| `ip` | Geolocate an IPv4/IPv6 address (country, city, coords, ISP, ASN, map link) — HTTPS with dual-provider failover |
| `domain` | Domain / WHOIS data via **RDAP**: registrar, creation/expiry dates, name servers, status, DNSSEC |
| `dns` | Resolve A / AAAA / MX / TXT / NS / CNAME / SOA records via **DNS-over-HTTPS** |
| `phone` | Phone-number intelligence: validity, line type, carrier, region, timezones, 4 formats (**offline**) |
| `username` | Hunt a username across **50+ sites concurrently** with per-site detection (status / body-text / redirect) and an honest **blocked** state for anti-bot sites |
| `email` | Passive email OSINT: syntax, MX (mail-capable domain), Gravatar |
| `web` | Website / HTTP recon: status, redirects, server, **security-header audit**, resolved IP |
| `mac` | MAC address → hardware **vendor** (OUI), local/multicast flags |
| `myip` | Discover and geolocate **your own** public IP |
| `update` | Upgrade dependencies and refresh the username site list (`--check` for a dry run) |

Every result can be exported with `--export json|csv|html`.

#### Reliable username detection

Naive "HTTP 200 = the profile exists" checks are wrong for most big platforms,
which answer `200` for every URL, redirect unknown users, or block bots. Argus
uses a per-site model (`errorType` in `data/sites.json`):

- **`status_code`** — exists only on a 2xx that was *not* redirected away.
- **`message`** — the page is always 200, so a marker string in the body decides.
- **`response_url`** — a missing profile is detected by its redirect target.

Anti-bot / rate-limit responses (401/403/406/429/451) are reported as
**`blocked`** — an explicit "unknown" — instead of being miscounted as found or
absent, so a result never claims more certainty than it has.

#### Staying up to date

```bash
argus update            # upgrade dependencies + refresh the site list
argus update --check    # report what's outdated, change nothing
argus update --sites    # refresh only the username catalogue
```

On launch, the interactive menu prints a **non-blocking** one-line hint when a
newer dependency release exists (cached once per day, disable with
`ARGUS_NO_UPDATE_CHECK=1`). Set `auto_update: true` in the config to upgrade
dependencies automatically at startup (opt-in — it needs the network and is
slower).

### 🚀 Installation

The installer auto-detects your OS, installs Python if needed, creates an
isolated virtual environment, installs Argus and adds an `argus` command to your
PATH. Full step-by-step guide: **[docs/INSTALL.md](docs/INSTALL.md)**.

**Ubuntu / Debian / macOS**
```bash
git clone https://github.com/chiaraberti13/prova.git argus
cd argus
./scripts/install.sh          # add --with-dns for real MX checks in the email module
argus                         # launch the interactive menu
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/chiaraberti13/prova.git argus
cd argus
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
argus
```

**Docker (no local Python needed)**
```bash
docker build -t argus .
docker run --rm -it argus                 # interactive menu
docker run --rm argus ip 8.8.8.8          # one-off command
```

### 🎯 Usage

Run `argus` for the **interactive menu**, or use **subcommands** for scripting:

```bash
argus ip 8.8.8.8
argus domain github.com
argus dns example.com --types A,MX,TXT
argus phone "+14155552671"
argus username torvalds --export html
argus email someone@example.com
argus web example.com
argus mac 3C:22:FB:11:22:33
argus myip
```

Global flags (before or after the subcommand): `--export {json,csv,html}`,
`--timeout SECONDS`, `--workers N`, `--no-color`.
Full reference: **[docs/USAGE.md](docs/USAGE.md)**.

### ⚙️ Configuration

Resolved in order: **CLI flags → environment variables → config file → defaults**.

| Setting | Flag | Env var | Default |
|---------|------|---------|---------|
| Request timeout (s) | `--timeout` | `ARGUS_TIMEOUT` | `8.0` |
| Concurrent workers | `--workers` | `ARGUS_MAX_WORKERS` | `20` |
| Retries | — | `ARGUS_RETRIES` | `2` |
| Output directory | — | `ARGUS_OUTPUT_DIR` | `<script folder>/report` |
| User-Agent | — | `ARGUS_USER_AGENT` | browser UA |
| Disable SSL verify | — | `ARGUS_NO_VERIFY_SSL=1` | (verify on) |
| Startup update hint | — | `ARGUS_NO_UPDATE_CHECK=1` | (check on) |
| Auto-upgrade on launch | — | `ARGUS_AUTO_UPDATE=1` | (off) |

```bash
argus config --init      # write ~/.config/argus/config.json
argus config --show      # print current settings
```

### 🗂️ Project structure

```
argus/
├── argus/                    # the Python package
│   ├── cli.py                # menu + CLI subcommands
│   ├── config.py             # layered configuration
│   ├── ui.py                 # rich UI with plain fallback
│   ├── exporters.py          # JSON / CSV / HTML reports
│   └── modules/              # ip · domain · dns · phone · username · email · web · mac · myip
├── data/sites.json           # 50+ username targets (easy to extend)
├── scripts/                  # install.sh · install.ps1 · run.sh · run.bat
├── docs/                     # INSTALL (EN/IT) · USAGE · DISCLAIMER
├── tests/                    # offline unit tests
├── Dockerfile · Makefile · pyproject.toml
└── .github/workflows/ci.yml  # CI on Ubuntu, macOS, Windows
```

Add a site to the username hunter by editing
[`data/sites.json`](data/sites.json) — no code changes needed.

### 🧪 Development

```bash
make venv     # create .venv and install with dev extras
make test     # run the offline test suite
make lint     # ruff
make run      # launch the menu
```

---

<a name="-italiano"></a>
## 🇮🇹 Italiano

### Cos'è Argus?

**Argus è un toolkit da riga di comando per l'OSINT (Open Source Intelligence)** —
la raccolta di informazioni da fonti *pubbliche e liberamente accessibili*.
Riunisce in **un'unica interfaccia veloce e coerente** i passi di ricognizione
che un analista compie di solito su una dozzina di siti e strumenti diversi, ed
esegue ogni ricerca in modo **passivo**: legge soltanto dati pubblici, senza mai
attaccare, autenticarsi o sondare sistemi privati.

Fornisci ad Argus un identificatore — un IP, un dominio, un numero di telefono,
uno username, un'email, un URL o un indirizzo MAC — e lo arricchisce con tutto
ciò che le fonti pubbliche sanno a riguardo, presentando il risultato in tabelle
colorate ordinate e potendo salvare un report in JSON / CSV / HTML.

**A chi serve e a cosa serve:**
- 🛡️ **Professionisti della sicurezza** — la fase di ricognizione di un
  penetration test o red-team *autorizzato* (mappare l'infrastruttura di un
  obiettivo).
- 🔎 **Threat intelligence e incident response** — arricchire rapidamente un
  indicatore (IP, dominio, hash di un'email) visto nei log o in un alert.
- 🕵️ **Analisti OSINT e investigatori** — ricostruire l'impronta digitale
  pubblica di un soggetto a partire da dati che ha scelto di rendere pubblici.
- 🙋 **Persone attente alla privacy** — verificare la *propria* esposizione:
  su quali siti compare il tuo username, cosa rivela il tuo IP pubblico, cosa
  lascia trapelare un dominio.
- 🎓 **Studenti e docenti** — un modo pratico e documentato per capire come
  funzionano davvero OSINT, DNS, WHOIS, HTTP e geolocalizzazione.

### 🧰 Moduli

| Comando | Cosa fa |
|---------|---------|
| `ip` | Geolocalizza un indirizzo IPv4/IPv6 (nazione, città, coordinate, ISP, ASN, link mappa) — HTTPS con failover su due provider |
| `domain` | Dati dominio / WHOIS via **RDAP**: registrar, date di creazione/scadenza, name server, stato, DNSSEC |
| `dns` | Record A / AAAA / MX / TXT / NS / CNAME / SOA via **DNS-over-HTTPS** |
| `phone` | Analisi numero: validità, tipo linea, operatore, regione, fusi orari, 4 formati (**offline**) |
| `username` | Cerca uno username su **50+ siti in parallelo** con rilevamento per-sito (status / testo / redirect) e uno stato **blocked** onesto per i siti anti-bot |
| `email` | OSINT email passivo: sintassi, MX (dominio in grado di ricevere posta), Gravatar |
| `web` | Ricognizione sito / HTTP: status, redirect, server, **audit degli header di sicurezza**, IP risolto |
| `mac` | Indirizzo MAC → **produttore** hardware (OUI), flag local/multicast |
| `myip` | Rileva e geolocalizza il **tuo** IP pubblico |
| `update` | Aggiorna le dipendenze e la lista siti username (`--check` per una prova a vuoto) |

Ogni risultato è esportabile con `--export json|csv|html`.

#### Rilevamento username affidabile

Il controllo ingenuo "HTTP 200 = il profilo esiste" è sbagliato per la maggior
parte delle grandi piattaforme, che rispondono `200` per qualsiasi URL,
reindirizzano gli utenti inesistenti o bloccano i bot. Argus usa un modello
per-sito (`errorType` in `data/sites.json`):

- **`status_code`** — esiste solo su un 2xx *non* reindirizzato altrove.
- **`message`** — la pagina è sempre 200, quindi decide una stringa nel corpo.
- **`response_url`** — un profilo assente si riconosce dalla destinazione del redirect.

Le risposte anti-bot / rate-limit (401/403/406/429/451) sono segnalate come
**`blocked`** — un "sconosciuto" esplicito — invece di essere contate come
trovate o assenti: così un risultato non pretende mai più certezza di quella che ha.

#### Restare aggiornati

```bash
argus update            # aggiorna dipendenze + ricarica la lista siti
argus update --check    # segnala cosa è obsoleto, senza modificare nulla
argus update --sites    # ricarica solo il catalogo username
```

All'avvio, il menu interattivo mostra un avviso **non bloccante** di una riga
quando esiste una versione più recente di una dipendenza (in cache una volta al
giorno, disattivabile con `ARGUS_NO_UPDATE_CHECK=1`). Imposta `auto_update: true`
nel config per aggiornare le dipendenze automaticamente all'avvio (opt-in —
richiede la rete ed è più lento).

### 🚀 Installazione

L'installer rileva automaticamente il sistema operativo, installa Python se
necessario, crea un ambiente virtuale isolato, installa Argus e aggiunge il
comando `argus` al PATH. Guida completa passo-passo: **[docs/INSTALL.it.md](docs/INSTALL.it.md)**.

**Ubuntu / Debian / macOS**
```bash
git clone https://github.com/chiaraberti13/prova.git argus
cd argus
./scripts/install.sh          # aggiungi --with-dns per controlli MX reali nel modulo email
argus                         # avvia il menu interattivo
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/chiaraberti13/prova.git argus
cd argus
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
argus
```

**Docker (senza Python installato in locale)**
```bash
docker build -t argus .
docker run --rm -it argus                 # menu interattivo
docker run --rm argus ip 8.8.8.8          # comando singolo
```

### 🎯 Utilizzo

Esegui `argus` per il **menu interattivo**, oppure usa i **sottocomandi** per lo scripting:

```bash
argus ip 8.8.8.8
argus domain github.com
argus dns example.com --types A,MX,TXT
argus phone "+390212345678"
argus username torvalds --export html
argus email qualcuno@example.com
argus web example.com
argus mac 3C:22:FB:11:22:33
argus myip
```

Flag globali (prima o dopo il sottocomando): `--export {json,csv,html}`,
`--timeout SECONDI`, `--workers N`, `--no-color`.
Riferimento completo: **[docs/USAGE.md](docs/USAGE.md)**.

### ⚙️ Configurazione

Risolta in quest'ordine: **flag CLI → variabili d'ambiente → file di config → default**.

| Impostazione | Flag | Variabile d'ambiente | Default |
|--------------|------|----------------------|---------|
| Timeout richiesta (s) | `--timeout` | `ARGUS_TIMEOUT` | `8.0` |
| Worker concorrenti | `--workers` | `ARGUS_MAX_WORKERS` | `20` |
| Retry | — | `ARGUS_RETRIES` | `2` |
| Cartella di output | — | `ARGUS_OUTPUT_DIR` | `<cartella script>/report` |
| User-Agent | — | `ARGUS_USER_AGENT` | UA browser |
| Disattiva verifica SSL | — | `ARGUS_NO_VERIFY_SSL=1` | (verifica attiva) |
| Avviso aggiornamenti all'avvio | — | `ARGUS_NO_UPDATE_CHECK=1` | (attivo) |
| Auto-aggiornamento all'avvio | — | `ARGUS_AUTO_UPDATE=1` | (disattivo) |

```bash
argus config --init      # crea ~/.config/argus/config.json
argus config --show      # mostra le impostazioni correnti
```

### 🗂️ Struttura del progetto

```
argus/
├── argus/                    # il pacchetto Python
│   ├── cli.py                # menu + comandi CLI
│   ├── config.py             # configurazione a livelli
│   ├── ui.py                 # UI colorata con fallback testuale
│   ├── exporters.py          # report JSON / CSV / HTML
│   └── modules/              # ip · domain · dns · phone · username · email · web · mac · myip
├── data/sites.json           # 50+ siti per username (facile da estendere)
├── scripts/                  # install.sh · install.ps1 · run.sh · run.bat
├── docs/                     # INSTALL (EN/IT) · USAGE · DISCLAIMER
├── tests/                    # test unitari offline
├── Dockerfile · Makefile · pyproject.toml
└── .github/workflows/ci.yml  # CI su Ubuntu, macOS, Windows
```

Aggiungi un sito alla ricerca username modificando
[`data/sites.json`](data/sites.json) — nessuna modifica al codice.

### 🧪 Sviluppo

```bash
make venv     # crea .venv e installa con gli extra di sviluppo
make test     # esegue i test offline
make lint     # ruff
make run      # avvia il menu
```

---

## 📄 License / Licenza

Released under the **[MIT License](LICENSE)**. Distribuito con **[Licenza MIT](LICENSE)**.

## ⚠️ Legal & ethical use / Uso legale ed etico

Argus queries only **publicly available** information and performs only
**passive** lookups. Use it exclusively on targets you own or are **explicitly
authorized** to investigate. Full terms: **[docs/DISCLAIMER.md](docs/DISCLAIMER.md)**.
