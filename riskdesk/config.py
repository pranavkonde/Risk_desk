from __future__ import annotations

import os
from pathlib import Path

MAINNET = "https://api.pacifica.fi/api/v1"
TESTNET = "https://test-api.pacifica.fi/api/v1"


def load_environment() -> None:
    """Load `.env` from repo root when `python-dotenv` is installed (no-op otherwise)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")


def rest_base() -> str:
    """
    REST API prefix. Override with PACIFICA_REST_URL, or set PACIFICA_NETWORK.
    PACIFICA_NETWORK: testnet | mainnet
    """
    override = os.environ.get("PACIFICA_REST_URL", "").strip()
    if override:
        return override.rstrip("/")
    env = os.environ.get("PACIFICA_NETWORK", "testnet").lower().strip()
    if env in ("main", "mainnet", "prod", "production"):
        return MAINNET
    return TESTNET
