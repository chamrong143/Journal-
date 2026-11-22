from decimal import Decimal as D
from gve.models import Trade
from gve.analytics.footprint import build_footprint

def test_footprint_aggregates_bid_ask_and_unknown():
    trades = [
        Trade(1, D("2350.04"), D("2"), "BUY"),
        Trade(2, D("2350.01"), D("1.5"), "SELL"),
        Trade(3, D("2350.00"), D("3"), "UNKNOWN"),
    ]
    rows = build_footprint(trades, D("0.1"))
    by_price = {r["price"]: r for r in rows}
    assert by_price[D("2350.0")]["ask_volume"] == D("2")
    assert by_price[D("2350.0")]["bid_volume"] == D("1.5")
    assert by_price[D("2350.0")]["unknown_volume"] == D("3")
    assert by_price[D("2350.0")]["delta"] == D("0.5")

def test_invalid_tick_rejected():
    try:
        build_footprint([], D("0"))
    except ValueError:
        pass
    else:
        assert False, "expected ValueError"
