from decimal import Decimal as D
from gve.models import Trade
from gve.analytics.delta import calculate_delta, calculate_cvd

def test_delta_and_cvd_ordering():
    trades = [Trade(3,D("10"),D("2"),"SELL"),
              Trade(1,D("10"),D("5"),"BUY"),
              Trade(2,D("10"),D("9"),"UNKNOWN")]
    d=calculate_delta(trades)
    assert d["delta"] == D("3")
    cvd=calculate_cvd(trades)
    assert [x["cvd"] for x in cvd] == [D("5"),D("5"),D("3")]
