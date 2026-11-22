from decimal import Decimal
from typing import Iterable

def detect_diagonal_imbalance(footprint: Iterable[dict], ratio: Decimal = Decimal("3")) -> list[dict]:
    """Compare ask at price P to bid one tick below; bid at P to ask one tick above.
    Input rows must be on a regular tick grid and include price/bid_volume/ask_volume.
    """
    if ratio <= 1:
        raise ValueError("imbalance ratio must be greater than 1")
    rows = sorted(list(footprint), key=lambda r: r["price"])
    by_price = {r["price"]: r for r in rows}
    if len(rows) < 2:
        return []
    tick = min((rows[i+1]["price"] - rows[i]["price"] for i in range(len(rows)-1)
                if rows[i+1]["price"] > rows[i]["price"]), default=None)
    if tick is None:
        return []
    out = []
    for r in rows:
        p = r["price"]
        below = by_price.get(p - tick)
        above = by_price.get(p + tick)
        ask = r["ask_volume"]
        bid = r["bid_volume"]
        ask_comp = below["bid_volume"] if below else Decimal("0")
        bid_comp = above["ask_volume"] if above else Decimal("0")
        ask_imb = ask > 0 and (ask_comp == 0 or ask >= ask_comp * ratio)
        bid_imb = bid > 0 and (bid_comp == 0 or bid >= bid_comp * ratio)
        if ask_imb or bid_imb:
            out.append({"price": p, "ask_imbalance": bool(ask_imb),
                        "bid_imbalance": bool(bid_imb), "ratio": ratio})
    return out

def find_stacked_imbalances(imbalances: Iterable[dict], min_levels: int = 3) -> list[dict]:
    if min_levels < 2:
        raise ValueError("min_levels must be at least 2")
    rows = sorted(imbalances, key=lambda r: r["price"])
    results = []
    for side in ("ask_imbalance", "bid_imbalance"):
        active = []
        for row in rows:
            if row.get(side):
                active.append(row["price"])
            else:
                if len(active) >= min_levels:
                    results.append({"side": side, "prices": active[:]})
                active = []
        if len(active) >= min_levels:
            results.append({"side": side, "prices": active[:]})
    return results
