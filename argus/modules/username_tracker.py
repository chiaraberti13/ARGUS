"""Concurrent username lookup across many platforms.

Features:
  * Loads its target list from ``data/sites.json`` (50+ sites, easy to extend).
  * Checks sites concurrently with a thread pool — dramatically faster.
  * Supports two detection strategies (HTTP status and body-text matching)
    to reduce false positives from sites that return 200 for everything.
  * Returns structured results suitable for export.
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from importlib import resources
from pathlib import Path
from typing import Callable, Iterable, Optional

from ..config import Config
from ..utils import build_session

_STATUS_FOUND = "found"
_STATUS_NOT_FOUND = "not found"
_STATUS_ERROR = "error"


def load_sites() -> list[dict]:
    """Load the site catalogue from the packaged/relative data file."""
    # Prefer a data/ dir next to the project root (dev / cloned repo).
    candidate = Path(__file__).resolve().parents[2] / "data" / "sites.json"
    if candidate.exists():
        data = json.loads(candidate.read_text(encoding="utf-8"))
        return data.get("sites", [])
    # Fallback: packaged data (if shipped inside the wheel).
    try:
        with resources.files("argus").joinpath("../data/sites.json").open(
            "r", encoding="utf-8"
        ) as fh:  # pragma: no cover
            return json.load(fh).get("sites", [])
    except Exception:  # pragma: no cover
        return []


def _check_one(session, site: dict, username: str, timeout: float) -> dict:
    url = site["url"].format(username=username)
    record = {
        "site": site["name"],
        "url": url,
        "category": site.get("category", "misc"),
        "status": _STATUS_ERROR,
        "http_status": None,
    }
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        record["http_status"] = resp.status_code
        method = site.get("method", "status")
        if method == "text":
            absence = site.get("absence", "")
            found = resp.status_code == 200 and absence not in resp.text
        else:
            found = resp.status_code == 200
        record["status"] = _STATUS_FOUND if found else _STATUS_NOT_FOUND
    except Exception as exc:  # network/timeouts are expected for some sites
        record["error"] = type(exc).__name__
    return record


def lookup(
    username: str,
    config: Optional[Config] = None,
    sites: Optional[Iterable[dict]] = None,
    on_result: Optional[Callable[[dict], None]] = None,
) -> dict:
    """Check ``username`` across all configured sites concurrently.

    ``on_result`` is called with each per-site record as it completes, enabling
    live UI updates. Returns a summary dict with the full list under ``results``.
    """
    config = config or Config.load()
    sites = list(sites) if sites is not None else load_sites()
    if not sites:
        return {"error": "no sites configured (data/sites.json missing?)", "username": username}

    session = build_session(config)
    results: list[dict] = []

    with ThreadPoolExecutor(max_workers=config.max_workers) as pool:
        futures = {
            pool.submit(_check_one, session, site, username, config.timeout): site
            for site in sites
        }
        for future in as_completed(futures):
            record = future.result()
            results.append(record)
            if on_result:
                on_result(record)

    results.sort(key=lambda r: (r["status"] != _STATUS_FOUND, r["site"].lower()))
    found = [r for r in results if r["status"] == _STATUS_FOUND]
    return {
        "username": username,
        "checked": len(results),
        "found_count": len(found),
        "results": results,
    }
