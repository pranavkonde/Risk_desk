"""
Fill- and market-level analytics derived from Pacifica REST payloads (client-side).
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def fills_to_dataframe(trades: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(trades) if trades else pd.DataFrame()


def summarize_fills(df: pd.DataFrame) -> tuple[dict[str, float | int], pd.DataFrame]:
    """Aggregate PnL and fees from `/trades/history` rows."""
    if df.empty:
        return {}, pd.DataFrame()

    work = df.copy()
    for col in ("pnl", "fee", "amount", "price", "entry_price"):
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors="coerce")

    total_pnl = float(work["pnl"].sum()) if "pnl" in work.columns else 0.0
    total_fee = float(work["fee"].sum()) if "fee" in work.columns else 0.0
    n = len(work)
    metrics: dict[str, float | int] = {
        "fills": n,
        "total_pnl": total_pnl,
        "total_fees": total_fee,
        "net_after_fees": total_pnl - total_fee,
    }

    if "symbol" not in work.columns:
        return metrics, pd.DataFrame()

    by_symbol = work.groupby("symbol", dropna=False).size().reset_index(name="fills")
    if "pnl" in work.columns:
        pnl_sum = work.groupby("symbol", dropna=False)["pnl"].sum().reset_index()
        by_symbol = by_symbol.merge(pnl_sum, on="symbol", how="left")
    if "fee" in work.columns:
        fee_sum = work.groupby("symbol", dropna=False)["fee"].sum().reset_index().rename(columns={"fee": "fees"})
        by_symbol = by_symbol.merge(fee_sum, on="symbol", how="left")
    if "pnl" in by_symbol.columns and "fees" in by_symbol.columns:
        by_symbol["net"] = by_symbol["pnl"] - by_symbol["fees"]
    if "pnl" in by_symbol.columns:
        by_symbol = by_symbol.sort_values("pnl", ascending=False, key=lambda s: s.abs(), na_position="last")
    else:
        by_symbol = by_symbol.sort_values("fills", ascending=False, na_position="last")

    return metrics, by_symbol.reset_index(drop=True)


def funding_extremes(df: pd.DataFrame, col: str = "next_funding", n: int = 8) -> pd.DataFrame:
    """Top markets by absolute funding (carry / crowding scan)."""
    if df.empty or col not in df.columns:
        return pd.DataFrame()
    work = df.copy()
    work[col] = pd.to_numeric(work[col], errors="coerce")
    work["_abs"] = work[col].abs()
    out = work.nlargest(n, "_abs")
    keep = [c for c in ("symbol", "mark", "mid", col, "open_interest", "volume_24h") if c in out.columns]
    return out[keep].reset_index(drop=True)


def order_book_spread(bids: pd.DataFrame, asks: pd.DataFrame) -> dict[str, float | None]:
    """Best bid / ask and spread from parsed book rows."""
    best_bid = best_ask = None
    if not bids.empty and "price" in bids.columns:
        best_bid = float(pd.to_numeric(bids["price"], errors="coerce").max())
    if not asks.empty and "price" in asks.columns:
        best_ask = float(pd.to_numeric(asks["price"], errors="coerce").min())
    spread = None
    if best_bid is not None and best_ask is not None:
        spread = best_ask - best_bid
    return {"best_bid": best_bid, "best_ask": best_ask, "spread": spread}


def position_risk_scorecard(positions: list[dict[str, Any]], marks: dict[str, Any]) -> dict[str, float]:
    """
    Lightweight portfolio risk signals from current positions and marks.
    All outputs are normalized to simple 0-100 style scores.
    """
    if not positions:
        return {
            "positions_count": 0.0,
            "gross_notional": 0.0,
            "largest_position_share_pct": 0.0,
            "concentration_score": 0.0,
            "directional_imbalance_pct": 0.0,
            "directional_risk_score": 0.0,
            "overall_risk_score": 0.0,
        }

    notionals: list[float] = []
    signed_notional = 0.0
    for p in positions:
        symbol = p.get("symbol")
        mark = pd.to_numeric(marks.get(symbol), errors="coerce")
        amount = pd.to_numeric(p.get("amount"), errors="coerce")
        entry = pd.to_numeric(p.get("entry_price"), errors="coerce")
        px = float(mark) if pd.notna(mark) and float(mark) > 0 else float(entry) if pd.notna(entry) else 0.0
        amt = float(amount) if pd.notna(amount) else 0.0
        notional = abs(amt * px)
        notionals.append(notional)
        side = str(p.get("side", "")).lower()
        sign = 1.0 if side in ("bid", "long", "buy", "b") else -1.0
        signed_notional += sign * notional

    gross_notional = sum(notionals)
    largest = max(notionals) if notionals else 0.0
    largest_share = (largest / gross_notional * 100.0) if gross_notional > 0 else 0.0
    directional_imbalance = (abs(signed_notional) / gross_notional * 100.0) if gross_notional > 0 else 0.0

    concentration_score = min(100.0, largest_share)
    directional_risk_score = min(100.0, directional_imbalance)
    overall = round(0.6 * concentration_score + 0.4 * directional_risk_score, 2)

    return {
        "positions_count": float(len(positions)),
        "gross_notional": float(gross_notional),
        "largest_position_share_pct": float(round(largest_share, 2)),
        "concentration_score": float(round(concentration_score, 2)),
        "directional_imbalance_pct": float(round(directional_imbalance, 2)),
        "directional_risk_score": float(round(directional_risk_score, 2)),
        "overall_risk_score": overall,
    }


def generate_insights(
    *,
    risk: dict[str, float],
    fill_metrics: dict[str, float | int],
    funding_table: pd.DataFrame,
    spread: dict[str, float | None] | None = None,
) -> list[str]:
    """Generate concise, demo-friendly trading insights from current analytics."""
    insights: list[str] = []

    overall = float(risk.get("overall_risk_score", 0.0))
    if overall >= 70:
        insights.append(
            f"Portfolio risk is elevated (score {overall:.1f}/100). Consider reducing concentration or directional skew."
        )
    elif overall >= 40:
        insights.append(
            f"Portfolio risk is moderate (score {overall:.1f}/100). Keep position sizing disciplined."
        )
    else:
        insights.append(f"Portfolio risk is contained (score {overall:.1f}/100).")

    net = float(fill_metrics.get("net_after_fees", 0.0))
    fees = float(fill_metrics.get("total_fees", 0.0))
    if net < 0 and fees > 0:
        insights.append("Recent trading window is net negative after fees; review execution quality and churn.")
    elif net > 0:
        insights.append("Recent trading window is net positive after fees.")

    if not funding_table.empty and "symbol" in funding_table.columns:
        col = "next_funding" if "next_funding" in funding_table.columns else None
        if col is None and "funding" in funding_table.columns:
            col = "funding"
        if col:
            top = funding_table.iloc[0]
            sym = str(top.get("symbol"))
            val = pd.to_numeric(top.get(col), errors="coerce")
            if pd.notna(val):
                insights.append(
                    f"Highest absolute funding signal is on {sym} ({col}={float(val):.6g}); monitor crowding risk."
                )

    if spread and spread.get("spread") is not None:
        insights.append(f"Current selected-book spread is {spread['spread']:.6g}.")

    return insights[:4]
