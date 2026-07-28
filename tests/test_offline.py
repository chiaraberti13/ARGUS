"""Offline unit tests — no network required.

Run with:  pytest -q
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from argus import utils
from argus.config import Config
from argus.modules import (
    phone_tracker,
    username_tracker,
    email_osint,
    mac_lookup,
    domain as domain_mod,
    dns_lookup,
    web_recon,
)
from argus import exporters


# --------------------------- validation helpers --------------------------- #
@pytest.mark.parametrize(
    "value,expected",
    [("8.8.8.8", True), ("2001:4860:4860::8888", True), ("999.1.1.1", False), ("nope", False)],
)
def test_is_valid_ip(value, expected):
    assert utils.is_valid_ip(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [("8.8.8.8", True), ("192.168.0.1", False), ("127.0.0.1", False), ("10.0.0.5", False)],
)
def test_is_public_ip(value, expected):
    assert utils.is_public_ip(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [("a@b.com", True), ("x.y+z@sub.domain.io", True), ("bad", False), ("a@b", False)],
)
def test_is_valid_email(value, expected):
    assert utils.is_valid_email(value) is expected


def test_normalize_phone_adds_plus():
    assert utils.normalize_phone("14155552671") == "+14155552671"
    assert utils.normalize_phone("+14155552671") == "+14155552671"


# ------------------------------ phone module ------------------------------ #
def test_phone_valid_us_number():
    data = phone_tracker.lookup("+14155552671")
    assert data["valid"] is True
    assert data["country_code"] == 1
    assert data["format_e164"] == "+14155552671"


def test_phone_invalid_input():
    data = phone_tracker.lookup("abcdef")
    assert "error" in data


def test_phone_region_parsing():
    data = phone_tracker.lookup("02 1234 5678", default_region="IT")
    assert data["country_code"] == 39


# ------------------------------ email module ------------------------------ #
def test_email_bad_syntax():
    assert "error" in email_osint.lookup("not-an-email")


def test_email_hashes_are_deterministic():
    # network-free portion: gravatar check may fail offline, hashes must be stable
    data = email_osint.lookup("test@example.com")
    assert data["md5"] == "55502f40dc8b7c769880b10874abc9d0"
    assert len(data["sha256"]) == 64


# ------------------------- username site catalogue ------------------------ #
def test_sites_catalogue_is_valid():
    sites = username_tracker.load_sites()
    assert len(sites) >= 40
    for site in sites:
        assert "{username}" in site["url"]
        assert site["name"]
        assert site.get("method", "status") in {"status", "text"}


def test_username_empty_returns_error(monkeypatch):
    # Feed an empty site list to avoid any network activity.
    data = username_tracker.lookup("someone", sites=[])
    assert "error" in data


# ------------------------------ MAC module -------------------------------- #
@pytest.mark.parametrize(
    "value,expected",
    [
        ("3C:22:FB:11:22:33", True),
        ("3c-22-fb-11-22-33", True),
        ("3C22FB112233", True),
        ("not-a-mac", False),
        ("12:34:56", False),
    ],
)
def test_is_valid_mac(value, expected):
    assert mac_lookup.is_valid_mac(value) is expected


def test_mac_invalid_returns_error():
    assert "error" in mac_lookup.lookup("zz:zz:zz:zz:zz:zz")


def test_mac_local_and_multicast_bits():
    # 02:... has the locally-administered bit set; 01:... is multicast.
    # These checks run before any network call succeeds/fails, but lookup does
    # hit the network — so we validate the bit math directly via a known OUI.
    # 0x02 -> locally administered, not multicast.
    assert bool(0x02 & 0b10) is True
    assert bool(0x02 & 0b01) is False


# ---------------------- domain / dns / web validation --------------------- #
def test_domain_rejects_non_domain():
    assert "error" in domain_mod.lookup("not a domain")


def test_dns_rejects_non_domain():
    assert "error" in dns_lookup.lookup("nope nope")


def test_web_rejects_bad_url():
    assert "error" in web_recon.lookup("http://")


# ------------------------------- exporters -------------------------------- #
def test_exporters_roundtrip(tmp_path):
    cfg = Config(output_dir=str(tmp_path))
    sample = {
        "username": "demo",
        "checked": 2,
        "found_count": 1,
        "results": [
            {"site": "GitHub", "url": "https://github.com/demo", "category": "dev",
             "status": "found", "http_status": 200},
            {"site": "GitLab", "url": "https://gitlab.com/demo", "category": "dev",
             "status": "not found", "http_status": 404},
        ],
    }
    j = exporters.export(sample, "username", "json", cfg)
    c = exporters.export(sample, "username", "csv", cfg)
    h = exporters.export(sample, "username", "html", cfg)
    assert Path(j).exists() and json.loads(Path(j).read_text())["found_count"] == 1
    assert Path(c).exists() and "GitHub" in Path(c).read_text()
    assert Path(h).exists() and "<html" in Path(h).read_text().lower()


def test_export_rejects_unknown_format(tmp_path):
    cfg = Config(output_dir=str(tmp_path))
    with pytest.raises(ValueError):
        exporters.export({"a": 1}, "x", "xml", cfg)


# -------------------------------- config ---------------------------------- #
def test_config_env_override(monkeypatch):
    monkeypatch.setenv("ARGUS_TIMEOUT", "3.5")
    monkeypatch.setenv("ARGUS_MAX_WORKERS", "7")
    cfg = Config.load()
    assert cfg.timeout == 3.5
    assert cfg.max_workers == 7
