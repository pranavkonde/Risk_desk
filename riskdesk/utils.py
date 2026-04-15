import json

import base58


def sort_json_keys(value):
    if isinstance(value, dict):
        return {k: sort_json_keys(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        return [sort_json_keys(item) for item in value]
    return value


def prepare_message(header, payload):
    if "type" not in header or "timestamp" not in header or "expiry_window" not in header:
        raise ValueError("Header must have type, timestamp, and expiry_window")
    data = {**header, "data": payload}
    message = sort_json_keys(data)
    return json.dumps(message, separators=(",", ":"))


def sign_message(header, payload, keypair):
    message = prepare_message(header, payload)
    message_bytes = message.encode("utf-8")
    signature = keypair.sign_message(message_bytes)
    return (message, base58.b58encode(bytes(signature)).decode("ascii"))
