from datetime import datetime, timezone
from gve.models import QualityReport

def assess_quality(*, provider_authenticated: bool, entitlement_verified: bool,
                   symbol_verified: bool, timestamps_valid: bool,
                   sequence_valid: bool, feed_timestamp: datetime | None,
                   max_staleness_seconds: float, licensing_reviewed: bool) -> QualityReport:
    errors = []
    fresh = False
    if feed_timestamp is None:
        errors.append("Missing feed timestamp")
    else:
        ts = feed_timestamp
        if ts.tzinfo is None:
            errors.append("Feed timestamp must be timezone-aware")
        else:
            age = (datetime.now(timezone.utc) - ts.astimezone(timezone.utc)).total_seconds()
            fresh = -2 <= age <= max_staleness_seconds
            if not fresh:
                errors.append(f"Feed stale or future-dated: age={age:.3f}s")
    flags = {
        "provider_authenticated": provider_authenticated,
        "entitlement_verified": entitlement_verified,
        "symbol_verified": symbol_verified,
        "timestamps_valid": timestamps_valid,
        "sequence_valid": sequence_valid,
        "licensing_reviewed": licensing_reviewed,
    }
    for name, ok in flags.items():
        if not ok:
            errors.append(f"Gate failed: {name}")
    return QualityReport(**flags, feed_fresh=fresh, errors=tuple(errors))
