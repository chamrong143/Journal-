from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable
from gve.models import Trade

def _tick_price(price: Decimal, tick_size: Decimal) -> Decimal:
    if tick_size <= 0:
        raise ValueError("tick_size must be positive")
    units = (price / tick_size).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return units * tick_size

def build_footprint(trades: Iterable[Trade], tick_size: Decimal) -> list[dict]:
    """Aggregate verified trade records by price. BUY=ask-initiated, SELL=bid-initiated."""
    if tick_size <= 0:
        raise ValueError("tick_size must be positive")
    levels = defaultdict(lambda: {"bid_volume": Decimal("0"), "ask_volume": Decimal("0"),
                                   "unknown_volume": Decimal("0"), "trade_count": 0})
    for trade in trades:
        if trade.size < 0 or trade.price <= 0:
            raise ValueError("Trade price must be positive and size cannot be negative")
        price = _tick_price(trade.price, tick_size)
        if trade.side == "BUY":
            levels[price]["ask_volume"] += trade.size
        elif trade.side == "SELL":
            levels[price]["bid_volume"] += trade.size
        else:
            levels[price]["unknown_volume"] += trade.size
        levels[price]["trade_count"] += 1

    result = []
    for price in sorted(levels, reverse=True):
        row = levels[price]
        row["price"] = price
        row["delta"] = row["ask_volume"] - row["bid_volume"]
        result.append(row)
    return result
