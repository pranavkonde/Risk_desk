import pandas as pd

from riskdesk.analytics import (
    fills_to_dataframe,
    generate_insights,
    order_book_spread,
    position_risk_scorecard,
    summarize_fills,
)


def test_summarize_fills_by_symbol():
    trades = [
        {"symbol": "BTC", "pnl": "1", "fee": "0.1", "side": "open_long"},
        {"symbol": "BTC", "pnl": "-0.5", "fee": "0.1", "side": "close_long"},
        {"symbol": "ETH", "pnl": "2", "fee": "0.2", "side": "open_short"},
    ]
    df = fills_to_dataframe(trades)
    metrics, by_sym = summarize_fills(df)
    assert metrics["fills"] == 3
    assert abs(metrics["total_pnl"] - 2.5) < 1e-9
    assert abs(metrics["total_fees"] - 0.4) < 1e-9
    assert "symbol" in by_sym.columns
    assert len(by_sym) == 2


def test_order_book_spread():
    bids = pd.DataFrame({"price": ["100", "99"], "side": ["bid"] * 2})
    asks = pd.DataFrame({"price": ["101", "102"], "side": ["ask"] * 2})
    sp = order_book_spread(bids, asks)
    assert sp["best_bid"] == 100.0
    assert sp["best_ask"] == 101.0
    assert sp["spread"] == 1.0


def test_position_risk_scorecard():
    positions = [
        {"symbol": "BTC", "side": "bid", "amount": "0.2", "entry_price": "70000"},
        {"symbol": "ETH", "side": "ask", "amount": "1.0", "entry_price": "3000"},
    ]
    marks = {"BTC": "71000", "ETH": "2900"}
    risk = position_risk_scorecard(positions, marks)
    assert risk["positions_count"] == 2.0
    assert risk["gross_notional"] > 0
    assert 0 <= risk["overall_risk_score"] <= 100


def test_generate_insights_non_empty():
    risk = {"overall_risk_score": 72.5}
    fill_metrics = {"net_after_fees": -10.0, "total_fees": 2.0}
    funding = pd.DataFrame([{"symbol": "BTC", "next_funding": 0.0002}])
    spread = {"spread": 1.5}
    insights = generate_insights(
        risk=risk,
        fill_metrics=fill_metrics,
        funding_table=funding,
        spread=spread,
    )
    assert len(insights) >= 2
