from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Optional

AggressorSide = Literal["BUY", "SELL", "UNKNOWN"]

@dataclass(frozen=True)
class Trade:
    timestamp_ns: int
    price: Decimal
    size: Decimal
    side: AggressorSide
    symbol: str = "GC"
    provider: str = "unknown"
    dataset: str = "unknown"
    quality: str = "UNVERIFIED"

@dataclass(frozen=True)
class QualityReport:
    provider_authenticated: bool
    entitlement_verified: bool
    symbol_verified: bool
    timestamps_valid: bool
    sequence_valid: bool
    feed_fresh: bool
    licensing_reviewed: bool
    errors: tuple[str, ...] = ()

    @property
    def trading_allowed(self) -> bool:
        return all((
            self.provider_authenticated,
            self.entitlement_verified,
            self.symbol_verified,
            self.timestamps_valid,
            self.sequence_valid,
            self.feed_fresh,
            self.licensing_reviewed,
        )) and not self.errors

    @property
    def status(self) -> str:
        return "VALID" if self.trading_allowed else "DATA INVALID — NO TRADE"
