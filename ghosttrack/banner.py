"""ASCII banner and program metadata."""
from __future__ import annotations

from . import __version__
from . import ui

BANNER = r"""
   ____ _               _     _____                _
  / ___| |__   ___  ___| |_  |_   _| __ __ _  ___| | __
 | |  _| '_ \ / _ \/ __| __|   | || '__/ _` |/ __| |/ /
 | |_| | | | | (_) \__ \ |_    | || | | (_| | (__|   <
  \____|_| |_|\___/|___/\__|   |_||_|  \__,_|\___|_|\_\
"""

TAGLINE = "OSINT & information-gathering toolkit — improved edition"


def show() -> None:
    if ui._RICH:  # colored gradient-ish banner
        ui.echo(f"[bold cyan]{BANNER}[/bold cyan]")
        ui.echo(f"        [bold white]{TAGLINE}[/bold white]")
        ui.echo(f"        [grey62]v{__version__} · authorized / educational use only[/grey62]\n")
    else:
        print(ui.C.CYAN + BANNER + ui.C.RESET)
        print(f"        {TAGLINE}")
        print(f"        v{__version__} - authorized / educational use only\n")
