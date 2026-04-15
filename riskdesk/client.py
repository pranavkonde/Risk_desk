from __future__ import annotations

import json
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from riskdesk.config import rest_base
from riskdesk.errors import PacificaAPIError

_sessions: dict[str, requests.Session] = {}


def _session_for(base: str) -> requests.Session:
    if base in _sessions:
        return _sessions[base]
    s = requests.Session()
    retries = Retry(
        total=4,
        connect=3,
        read=3,
        backoff_factor=0.4,
        status_forcelist=(502, 503, 504),
        allowed_methods=("GET", "POST"),
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({"Accept": "application/json"})
    _sessions[base] = s
    return s


def _parse_body(r: requests.Response) -> Any:
    text = (r.text or "").strip()
    if not text:
        return None
    ct = (r.headers.get("Content-Type") or "").lower()
    if "json" in ct or text.startswith("{") or text.startswith("["):
        try:
            return r.json()
        except json.JSONDecodeError:
            return None
    return text


def _get(path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    base = rest_base().rstrip("/")
    url = f"{base}/{path.lstrip('/')}"
    session = _session_for(base)
    try:
        r = session.get(url, params=params or {}, timeout=30)
    except requests.RequestException as e:
        raise PacificaAPIError(f"Request failed: {e}", http_status=None) from e

    body = _parse_body(r)
    if r.status_code >= 400:
        msg = body if isinstance(body, str) else (body or {})
        raise PacificaAPIError(
            f"HTTP {r.status_code}: {msg}",
            http_status=r.status_code,
            body_text=r.text[:2000] if isinstance(body, str) else None,
        )

    if not isinstance(body, dict):
        raise PacificaAPIError("Unexpected response (not a JSON object)", http_status=r.status_code)

    if not body.get("success"):
        err = body.get("error") or body.get("code") or body
        raise PacificaAPIError(f"API error: {err}", http_status=r.status_code)

    return body


def market_info() -> list[dict[str, Any]]:
    return _get("info")["data"]


def market_prices() -> list[dict[str, Any]]:
    return _get("info/prices")["data"]


def order_book(symbol: str) -> dict[str, Any]:
    return _get("book", {"symbol": symbol})["data"]


def account(pubkey: str) -> dict[str, Any]:
    return _get("account", {"account": pubkey})["data"]


def positions(pubkey: str) -> list[dict[str, Any]]:
    return _get("positions", {"account": pubkey})["data"]


def trade_history(pubkey: str, limit: int = 100) -> tuple[list[dict[str, Any]], bool, str | None]:
    body = _get("trades/history", {"account": pubkey, "limit": str(limit)})
    return (
        body.get("data") or [],
        bool(body.get("has_more")),
        body.get("next_cursor"),
    )
