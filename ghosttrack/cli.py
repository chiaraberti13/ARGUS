"""Command-line interface: interactive menu + scriptable subcommands."""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from . import __version__, banner, ui
from .config import Config
from .exporters import export
from .modules import email_osint, ip_tracker, myip, phone_tracker, username_tracker

DISCLAIMER = (
    "GhostTrack is provided for authorized security research, OSINT training and "
    "educational purposes only. You are solely responsible for complying with all "
    "applicable laws. Only gather information you are legally permitted to access."
)


# --------------------------------------------------------------------------- #
# Rendering helpers
# --------------------------------------------------------------------------- #
def _maybe_export(data: dict, kind: str, config: Config, fmt: Optional[str]) -> None:
    if not fmt or fmt == "none":
        return
    try:
        path = export(data, kind, fmt, config)
        ui.success(f"Report saved: {path}")
    except Exception as exc:
        ui.error(f"Export failed: {exc}")


def render_ip(data: dict) -> None:
    if "error" in data:
        ui.error(data["error"])
        return
    if data.get("warning"):
        ui.warn(data["warning"])
    rows = [
        ("IP", data.get("ip")),
        ("Type", data.get("type")),
        ("Country", f"{data.get('country')} ({data.get('country_code')})"),
        ("Region", data.get("region")),
        ("City", data.get("city")),
        ("Postal", data.get("postal")),
        ("Coordinates", f"{data.get('latitude')}, {data.get('longitude')}"),
        ("Timezone", f"{data.get('timezone')} {data.get('utc_offset') or ''}".strip()),
        ("ISP", data.get("isp")),
        ("Organization", data.get("org")),
        ("ASN", data.get("asn")),
        ("Google Maps", data.get("google_maps")),
        ("Source", data.get("source")),
    ]
    ui.kv_table([(k, v) for k, v in rows if v not in (None, "None")], title="IP Geolocation")


def render_phone(data: dict) -> None:
    if "error" in data:
        ui.error(data["error"])
        return
    if data.get("warning"):
        ui.warn(data["warning"])
    tz = data.get("timezones")
    rows = [
        ("Input", data.get("input")),
        ("Valid", "yes" if data.get("valid") else "no"),
        ("Possible", "yes" if data.get("possible") else "no"),
        ("Country code", f"+{data.get('country_code')}"),
        ("Line type", data.get("line_type")),
        ("Region", data.get("region")),
        ("Carrier", data.get("carrier")),
        ("Timezone(s)", ", ".join(tz) if tz else None),
        ("E.164", data.get("format_e164")),
        ("International", data.get("format_international")),
        ("National", data.get("format_national")),
        ("RFC3966", data.get("format_rfc3966")),
    ]
    ui.kv_table([(k, v) for k, v in rows if v], title="Phone Intelligence")


def render_username(data: dict) -> None:
    if "error" in data:
        ui.error(data["error"])
        return
    found = [r for r in data["results"] if r["status"] == "found"]
    ui.results_table(
        ["Site", "Category", "URL"],
        [(r["site"], r["category"], r["url"]) for r in found],
        title=f"'{data['username']}' found on {data['found_count']}/{data['checked']} sites",
    )
    if not found:
        ui.warn("No profiles found (or all sites blocked automated checks).")


def render_email(data: dict) -> None:
    if "error" in data:
        ui.error(data["error"])
        return
    mx = data.get("domain_has_mx")
    rows = [
        ("Email", data.get("email")),
        ("Local part", data.get("local_part")),
        ("Domain", data.get("domain")),
        ("Valid syntax", "yes" if data.get("valid_syntax") else "no"),
        ("Domain has MX", {True: "yes", False: "no", None: "unknown"}[mx]),
        ("Gravatar exists", {True: "yes", False: "no", None: "unknown"}[data.get("gravatar_exists")]),
        ("Gravatar URL", data.get("gravatar_url") if data.get("gravatar_exists") else None),
        ("MD5", data.get("md5")),
        ("SHA-256", data.get("sha256")),
    ]
    ui.kv_table([(k, v) for k, v in rows if v is not None], title="Email OSINT")


def render_myip(data: dict) -> None:
    if "error" in data:
        ui.error(data["error"])
        return
    ui.kv_table([("Public IP", data["public_ip"])], title="Your Public IP")
    if data.get("geo"):
        render_ip(data["geo"])


# --------------------------------------------------------------------------- #
# Interactive menu
# --------------------------------------------------------------------------- #
MENU = """
  [bold cyan]1[/bold cyan]  IP address geolocation
  [bold cyan]2[/bold cyan]  Phone number intelligence
  [bold cyan]3[/bold cyan]  Username lookup (50+ sites)
  [bold cyan]4[/bold cyan]  Email OSINT
  [bold cyan]5[/bold cyan]  Show my public IP
  [bold cyan]6[/bold cyan]  Settings
  [bold cyan]0[/bold cyan]  Exit
"""


def _ask_export(config: Config) -> Optional[str]:
    choice = ui.prompt("Export report? [n]one / json / csv / html:").strip().lower()
    return choice if choice in {"json", "csv", "html"} else None


def interactive(config: Config) -> int:
    ui.clear()
    banner.show()
    ui.panel(DISCLAIMER, title="Legal notice")
    while True:
        ui.echo(MENU)
        try:
            choice = ui.prompt("ghosttrack ›").strip()
        except (EOFError, KeyboardInterrupt):
            ui.echo("\nBye.")
            return 0

        try:
            if choice == "1":
                ip = ui.prompt("Target IP address:")
                data = ip_tracker.lookup(ip, config)
                render_ip(data)
                _maybe_export(data, "ip", config, _ask_export(config))
            elif choice == "2":
                num = ui.prompt("Phone number (+country...):")
                data = phone_tracker.lookup(num)
                render_phone(data)
                _maybe_export(data, "phone", config, _ask_export(config))
            elif choice == "3":
                user = ui.prompt("Username to search:")
                data = _run_username(user, config)
                render_username(data)
                _maybe_export(data, "username", config, _ask_export(config))
            elif choice == "4":
                email = ui.prompt("Email address:")
                data = email_osint.lookup(email, config)
                render_email(data)
                _maybe_export(data, "email", config, _ask_export(config))
            elif choice == "5":
                data = myip.my_ip(config)
                render_myip(data)
            elif choice == "6":
                _settings_menu(config)
            elif choice in {"0", "q", "exit", "quit"}:
                ui.echo("Bye.")
                return 0
            else:
                ui.warn("Unknown option.")
        except KeyboardInterrupt:
            ui.warn("Cancelled.")
        ui.echo()


def _run_username(user: str, config: Config) -> dict:
    if not user.strip():
        return {"error": "empty username", "username": user}
    sites = username_tracker.load_sites()
    ui.info(f"Checking {len(sites)} sites for '{user}' …")
    collected: list[dict] = []

    def _sink(_record):
        collected.append(_record)

    # Drive the lookup while showing a progress bar.
    result_holder: dict = {}

    def _worker():
        result_holder.update(username_tracker.lookup(user, config, sites, on_result=_sink))

    import threading

    t = threading.Thread(target=_worker)
    t.start()
    total = len(sites)
    for _ in ui.progress_iter(_wait_progress(collected, total), "Scanning", total=total):
        pass
    t.join()
    return result_holder


def _wait_progress(collected: list, total: int):
    """Yield once per completed site so the progress bar advances live."""
    import time

    seen = 0
    while seen < total:
        current = len(collected)
        while seen < current:
            seen += 1
            yield seen
        time.sleep(0.05)


def _settings_menu(config: Config) -> None:
    rows = [
        ("timeout", config.timeout),
        ("max_workers", config.max_workers),
        ("retries", config.retries),
        ("verify_ssl", config.verify_ssl),
        ("output_dir", config.output_dir),
        ("user_agent", config.user_agent),
    ]
    ui.kv_table(rows, title="Current settings")
    ui.info("Edit config file to persist changes: use 'ghosttrack config --show'.")


# --------------------------------------------------------------------------- #
# Argument parsing / non-interactive subcommands
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    # Options shared by every subcommand (accepted before OR after the target).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--no-color",
        action="store_true",
        default=argparse.SUPPRESS,
        help="disable colored output",
    )
    common.add_argument(
        "--export",
        choices=["json", "csv", "html"],
        default=argparse.SUPPRESS,
        help="export result to a report",
    )
    common.add_argument(
        "--timeout",
        type=float,
        default=argparse.SUPPRESS,
        help="per-request timeout in seconds",
    )
    common.add_argument(
        "--workers",
        type=int,
        default=argparse.SUPPRESS,
        help="max concurrent workers (username lookup)",
    )

    p = argparse.ArgumentParser(
        prog="ghosttrack",
        description="GhostTrack — improved cross-platform OSINT toolkit.",
        epilog="Run without a subcommand to launch the interactive menu.",
        parents=[common],
    )
    p.add_argument("--version", action="version", version=f"GhostTrack {__version__}")

    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("ip", help="geolocate an IP address", parents=[common])
    sp.add_argument("address")

    sp = sub.add_parser("phone", help="analyze a phone number", parents=[common])
    sp.add_argument("number")
    sp.add_argument("--region", help="default ISO region, e.g. US, IT, GB")

    sp = sub.add_parser("username", help="search a username across sites", parents=[common])
    sp.add_argument("name")

    sp = sub.add_parser("email", help="passive email OSINT", parents=[common])
    sp.add_argument("address")

    sub.add_parser("myip", help="show this machine's public IP", parents=[common])

    sp = sub.add_parser("config", help="show or initialize configuration", parents=[common])
    sp.add_argument("--show", action="store_true", help="print current config")
    sp.add_argument("--init", action="store_true", help="write a default config file")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    export_fmt = getattr(args, "export", None)
    timeout = getattr(args, "timeout", None)
    workers = getattr(args, "workers", None)

    config = Config.load()
    if timeout:
        config.timeout = timeout
    if workers:
        config.max_workers = workers

    if not args.command:
        return interactive(config)

    if args.command == "ip":
        data = ip_tracker.lookup(args.address, config)
        render_ip(data)
        _maybe_export(data, "ip", config, export_fmt)
    elif args.command == "phone":
        data = phone_tracker.lookup(args.number, getattr(args, "region", None))
        render_phone(data)
        _maybe_export(data, "phone", config, export_fmt)
    elif args.command == "username":
        data = username_tracker.lookup(args.name, config)
        render_username(data)
        _maybe_export(data, "username", config, export_fmt)
    elif args.command == "email":
        data = email_osint.lookup(args.address, config)
        render_email(data)
        _maybe_export(data, "email", config, export_fmt)
    elif args.command == "myip":
        data = myip.my_ip(config)
        render_myip(data)
        _maybe_export(data, "myip", config, export_fmt)
    elif args.command == "config":
        if args.init:
            path = config.save()
            ui.success(f"Config written to {path}")
        else:
            _settings_menu(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
