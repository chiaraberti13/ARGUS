# 📦 Guida all'Installazione (Italiano)

> 🇬🇧 English version: [INSTALL.md](INSTALL.md)

Questa guida copre **Windows**, **Ubuntu/Debian Linux** e **macOS**, sia con
l'installer automatico da un solo comando sia con le istruzioni manuali
passo-passo, oltre alla risoluzione dei problemi.

- [Requisiti](#requisiti)
- [Ubuntu / Debian Linux](#-ubuntu--debian-linux)
- [macOS](#-macos)
- [Windows](#-windows)
- [Docker (qualsiasi sistema)](#-docker-qualsiasi-sistema)
- [Verifica dell'installazione](#-verifica-dellinstallazione)
- [Aggiornamento](#-aggiornamento)
- [Disinstallazione](#-disinstallazione)
- [Risoluzione dei problemi](#-risoluzione-dei-problemi)

---

## Requisiti

- **Python 3.8 o successivo** (gli installer possono installarlo per te)
- **git** (per clonare il repository)
- Accesso a Internet (lo strumento interroga servizi OSINT pubblici)

Tutto il resto (`requests`, `phonenumbers`, `rich`) viene installato
automaticamente in un ambiente virtuale isolato, così il Python di sistema
rimane pulito.

---

## 🐧 Ubuntu / Debian Linux

### Opzione A — Automatica (consigliata)

```bash
# 1. Installa git se non presente
sudo apt update && sudo apt install -y git

# 2. Clona il progetto
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack

# 3. Avvia l'installer (usa sudo solo se Python/venv mancano)
./scripts/install.sh

# Varianti opzionali:
./scripts/install.sh --with-dns    # abilita i controlli MX reali (modulo email)
./scripts/install.sh --dev         # installa anche pytest + ruff per lo sviluppo
```

Lo script eseguirà:
1. Rilevamento di Ubuntu/Debian e verifica di Python 3.8+, `venv` e `pip`
   (installandoli con `apt` se mancanti).
2. Creazione di un ambiente virtuale in `./.venv`.
3. Installazione di GhostTrack e delle sue dipendenze.
4. Creazione di un launcher `ghosttrack` in `~/.local/bin` e aggiunta al `PATH`.

Poi basta eseguire:
```bash
ghosttrack
```
Se il comando non viene trovato, ricarica la shell: `source ~/.bashrc` (o apri un nuovo terminale).

### Opzione B — Manuale

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m ghosttrack        # esecuzione
```

---

## 🍎 macOS

### Opzione A — Automatica (consigliata)

```bash
# Se non hai Homebrew, installalo prima (consigliato):
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
chmod +x scripts/install.sh
./scripts/install.sh
```

L'installer userà **Homebrew** per installare Python se mancante. Se non usi
Homebrew, installa prima Python 3.8+ da [python.org](https://www.python.org/downloads/macos/)
e poi riavvia lo script.

Avvio:
```bash
ghosttrack
```
Se non trovato, aggiungi la cartella del launcher al profilo della shell:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Opzione B — Manuale

```bash
brew install python git          # oppure installa Python da python.org
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m ghosttrack
```

---

## 🪟 Windows

### Opzione A — Automatica (consigliata)

1. Installa **Git per Windows**: <https://git-scm.com/download/win>
   (Python è opzionale — l'installer può scaricarlo tramite `winget`.)
2. Apri **PowerShell** ed esegui:

```powershell
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
powershell -ExecutionPolicy Bypass -File scripts\install.ps1

# Varianti opzionali:
#   -WithDns   abilita i controlli MX reali
#   -Dev       installa pytest + ruff
```

Lo script eseguirà:
1. Ricerca di Python 3.8+ (o installazione di Python 3.12 tramite `winget` se mancante).
2. Creazione di un ambiente virtuale in `.\.venv`.
3. Installazione di GhostTrack.
4. Creazione di `ghosttrack.cmd` in `%LOCALAPPDATA%\Programs\GhostTrack\bin` e aggiunta al `PATH` utente.

**Apri un nuovo terminale**, poi:
```powershell
ghosttrack
```

> Se compare *"running scripts is disabled on this system"*, hai avviato
> PowerShell con `-ExecutionPolicy Bypass` (come sopra — consigliato) oppure
> puoi abilitare gli script per l'utente una volta sola:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Opzione B — Manuale

```powershell
# Installa Python 3.8+ da https://python.org (spunta "Add python.exe to PATH")
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
python -m ghosttrack
```

---

## 🐳 Docker (qualsiasi sistema)

Non serve Python in locale — basta Docker.

```bash
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack
docker build -t ghosttrack .

# Menu interattivo
docker run --rm -it ghosttrack

# Comando singolo
docker run --rm ghosttrack username torvalds

# Salva i report sull'host (monta un volume)
docker run --rm -v "$PWD/reports:/reports" ghosttrack ip 8.8.8.8 --export html
```

---

## ✅ Verifica dell'installazione

```bash
ghosttrack --version                 # stampa: GhostTrack 3.0.0
ghosttrack phone "+390212345678"     # funziona offline — ottimo test rapido
```

Se il comando `ghosttrack` non viene trovato, puoi sempre eseguirlo esplicitamente:
```bash
# Linux/macOS
.venv/bin/python -m ghosttrack
# Windows
.venv\Scripts\python.exe -m ghosttrack
```

---

## 🔄 Aggiornamento

```bash
cd GhostTrack
git pull
# poi riavvia l'installer (idempotente) oppure, dentro il venv:
pip install -e . --upgrade
```

---

## 🧹 Disinstallazione

```bash
# Rimuovi l'ambiente virtuale e i report
rm -rf .venv ~/ghosttrack-reports          # Windows: rmdir /s .venv

# Rimuovi il launcher
rm ~/.local/bin/ghosttrack                 # Linux/macOS
# Windows: elimina %LOCALAPPDATA%\Programs\GhostTrack e rimuovilo dal PATH

# Infine elimina la cartella clonata
cd .. && rm -rf GhostTrack
```

---

## 🛠️ Risoluzione dei problemi

| Sintomo | Soluzione |
|---------|-----------|
| `ghosttrack: command not found` | Apri un nuovo terminale, oppure aggiungi `~/.local/bin` (Linux/macOS) / la cartella del launcher (Windows) al `PATH`. Puoi sempre usare `python -m ghosttrack` dentro il venv. |
| `python3: command not found` (Linux) | `sudo apt install python3 python3-venv python3-pip` |
| Errore pip `externally-managed-environment` | È previsto sulle distro moderne — proprio per questo usiamo un **ambiente virtuale**. Non installare con pip a livello globale; usa l'installer o il venv. |
| PowerShell: *running scripts is disabled* | Esegui con `-ExecutionPolicy Bypass` (mostrato sopra) o `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. |
| Errori SSL / proxy dietro un proxy aziendale | Imposta `HTTPS_PROXY`, o come ultima risorsa `GHOSTTRACK_NO_VERIFY_SSL=1` (sconsigliato). |
| I risultati username sembrano falsi positivi | Alcuni siti rispondono HTTP 200 a qualsiasi URL. Aumenta `--timeout`, oppure affina la voce del sito in `data/sites.json` usando il metodo di rilevamento `text`. |
| Il modulo email indica MX = *unknown* | Installa la dipendenza opzionale: `pip install dnspython` (o reinstalla con `--with-dns`). |

Problemi persistenti? Apri una issue indicando sistema operativo, versione di
Python (`python3 --version`) e il messaggio d'errore esatto.
