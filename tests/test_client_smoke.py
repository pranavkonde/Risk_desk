"""Live smoke tests against Pacifica testnet (skipped when PACIFICA_SMOKE_TESTS=0)."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("PACIFICA_NETWORK", "testnet")


@pytest.mark.skipif(
    os.environ.get("PACIFICA_SMOKE_TESTS", "1").lower() in ("0", "false", "no"),
    reason="PACIFICA_SMOKE_TESTS disabled",
)
def test_market_info_returns_rows():
    from riskdesk import client

    rows = client.market_info()
    assert isinstance(rows, list)
    assert len(rows) >= 1
    assert "symbol" in rows[0]


@pytest.mark.skipif(
    os.environ.get("PACIFICA_SMOKE_TESTS", "1").lower() in ("0", "false", "no"),
    reason="PACIFICA_SMOKE_TESTS disabled",
)
def test_order_book_btc():
    from riskdesk import client

    ob = client.order_book("BTC")
    assert "l" in ob
