from collections import defaultdict
from decimal import Decimal
from typing import Iterable
from gve.models import Trade

def build_volume_profile(trades: Iterable[Trade], tick_size: Decimal,
                         value_area_pct: Decimal = Decimal("70")) -> dict:
    if tick_size <= 0:
        raise ValueError("tick_size must be positive")
    if not (Decimal("50") <= value_area_pct <= Decimal("90")):
        raise ValueError("value_area_pct must be between 50 and 90")
    volume = defaultdict(lambda: Decimal("0"))
    for t in trades:
        if t.side == "UNKNOWN":
            # Trade size is real volume but unknown aggressor side; it still belongs in total volume.
            pass
        if t.price <= 0 or t.size < 0:
            raise ValueError("Invalid trade")
        units = (t.price / tick_size).quantize(Decimal("1"))
        price = units * tick_size
        volume[price] += t.size
    if not volume:
        return {"poc": None, "vah": None, "val": None, "total_volume": Decimal("0"), "levels": []}
    prices = sorted(volume)
    poc = max(prices, key=lambda p: (volume[p], -prices.index(p)))
    total = sum(volume.values(), Decimal("0"))
    target = total * value_area_pct / Decimal("100")
    included = {poc}
    accumulated = volume[poc]
    lo = hi = prices.index(poc)
    # Expand to the adjacent price level with larger volume until value-area target is reached.
    while accumulated < target and (lo > 0 or hi < len(prices)-1):
        down = volume[prices[lo-1]] if lo > 0 else Decimal("-1")
        up = volume[prices[hi+1]] if hi < len(prices)-1 else Decimal("-1")
        if up > down:
            hi += 1
            chosen = prices[hi]
        else:
            lo -= 1
            chosen = prices[lo]
        included.add(chosen)
        accumulated += volume[chosen]
    return {"poc": poc, "vah": max(included), "val": min(included),
            "total_volume": total,
            "levels": [{"price": p, "volume": volume[p]} for p in prices]}
