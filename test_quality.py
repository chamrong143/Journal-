from datetime import datetime, timezone
from gve.quality import assess_quality

def test_quality_blocks_if_any_gate_fails():
    q=assess_quality(provider_authenticated=True, entitlement_verified=False,
        symbol_verified=True, timestamps_valid=True, sequence_valid=True,
        feed_timestamp=datetime.now(timezone.utc), max_staleness_seconds=10,
        licensing_reviewed=True)
    assert not q.trading_allowed
    assert q.status == "DATA INVALID — NO TRADE"

def test_quality_passes_only_all_gates():
    q=assess_quality(provider_authenticated=True, entitlement_verified=True,
        symbol_verified=True, timestamps_valid=True, sequence_valid=True,
        feed_timestamp=datetime.now(timezone.utc), max_staleness_seconds=10,
        licensing_reviewed=True)
    assert q.trading_allowed
