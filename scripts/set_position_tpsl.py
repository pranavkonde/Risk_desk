#!/usr/bin/env python3
"""
Set TP/SL on an open position (Pacifica REST POST /positions/tpsl).
Requires PACIFICA_PRIVATE_KEY (base58) and PACIFICA_NETWORK=testnet|mainnet.

Example:
  export PACIFICA_PRIVATE_KEY='...'
  export PACIFICA_NETWORK=testnet
  python scripts/set_position_tpsl.py --symbol BTC --side ask \\
    --tp-stop 120000 --tp-limit 120300 --tp-amount 0.1 \\
    --sl-stop 99800
"""

from __future__ import annotations

import argparse
import os
import time
import uuid

import requests
from solders.keypair import Keypair

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from riskdesk.config import load_environment, rest_base
from riskdesk.utils import sign_message


def main() -> None:
    load_environment()
    pk = os.environ.get("PACIFICA_PRIVATE_KEY", "").strip()
    if not pk:
        raise SystemExit("Set PACIFICA_PRIVATE_KEY to your wallet base58 secret.")

    p = argparse.ArgumentParser()
    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True, help="Position side: bid (long) or ask (short)")
    p.add_argument("--tp-stop", dest="tp_stop", default=None)
    p.add_argument("--tp-limit", dest="tp_limit", default=None)
    p.add_argument("--tp-amount", dest="tp_amount", default=None)
    p.add_argument("--sl-stop", dest="sl_stop", default=None)
    p.add_argument("--sl-limit", dest="sl_limit", default=None)
    p.add_argument("--sl-amount", dest="sl_amount", default=None)
    args = p.parse_args()

    keypair = Keypair.from_base58_string(pk)
    public_key = str(keypair.pubkey())
    ts = int(time.time() * 1_000)
    header = {"timestamp": ts, "expiry_window": 5_000, "type": "set_position_tpsl"}

    take_profit = None
    if args.tp_stop:
        take_profit = {"stop_price": args.tp_stop, "client_order_id": str(uuid.uuid4())}
        if args.tp_limit:
            take_profit["limit_price"] = args.tp_limit
        if args.tp_amount:
            take_profit["amount"] = args.tp_amount

    stop_loss = None
    if args.sl_stop:
        stop_loss = {"stop_price": args.sl_stop}
        if args.sl_limit:
            stop_loss["limit_price"] = args.sl_limit
        if args.sl_amount:
            stop_loss["amount"] = args.sl_amount

    payload: dict = {"symbol": args.symbol, "side": args.side}
    if take_profit:
        payload["take_profit"] = take_profit
    if stop_loss:
        payload["stop_loss"] = stop_loss

    message, signature = sign_message(header, payload, keypair)
    req = {
        "account": public_key,
        "signature": signature,
        "timestamp": header["timestamp"],
        "expiry_window": header["expiry_window"],
        **payload,
    }
    url = f"{rest_base()}/positions/tpsl"
    r = requests.post(url, json=req, headers={"Content-Type": "application/json"}, timeout=30)
    print(r.status_code, r.text)


if __name__ == "__main__":
    main()
