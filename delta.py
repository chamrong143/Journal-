from decimal import Decimal
from typing import Iterable
from gve.models import Trade

def calculate_delta(trades: Iterable[Trade]) -> dict:
    buy = sell = unknown = Decimal("0")
    count = 0
    for t in trades:
        count += 1
        if t.side == "BUY":
            buy += t.size
        elif t.side == "SELL":
            sell += t.size
        else:
            unknown += t.size
    return {"ask_initiated_volume": buy, "bid_initiated_volume": sell,
            "unknown_volume": unknown, "delta": buy - sell, "trade_count": count}

def calculate_cvd(trades: Iterable[Trade]) -> list[dict]:
    """Return cumulative delta in event-time order; UNKNOWN trades do not change CVD."""
    ordered = sorted(trades, key=lambda t: t.timestamp_ns)
    running = Decimal("0")
    out = []
    for t in ordered:
        change = t.size if t.side == "BUY" else (-t.size if t.side == "SELL" else Decimal("0"))
        running += change
        out.append({"timestamp_ns": t.timestamp_ns, "delta": change, "cvd": running})
    return out
