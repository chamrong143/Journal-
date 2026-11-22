# GVE Order Flow Data Contract (Draft)

## Trade record
- provider: string
- dataset: string
- instrument_id: integer/string
- raw_symbol: string
- event_time_ns: integer (UTC)
- receive_time_ns: integer (UTC)
- price: decimal
- size: decimal
- aggressor_side: BUY | SELL | UNKNOWN
- source_schema: trades | tbbo | other
- quality: UNVERIFIED | VALIDATED
- contract_expiry: optional date

## Market depth event
- provider, dataset, instrument_id, event_time_ns, receive_time_ns
- action: ADD | MODIFY | CANCEL | CLEAR | SNAPSHOT
- side: BID | ASK
- price, size, order_id (when MBO)
- sequence_number
- schema: MBO | MBP10

## Spot quote
- provider, symbol, timestamp_ns, bid, ask, mid/last
- quality and source plan

## Quality gates
- Provider authentication and subscription entitlement checked server-side.
- Instrument mapping and contract expiry confirmed.
- UTC event and receive timestamps checked.
- Duplicate and sequence-gap detection.
- Stale-feed threshold.
- GC/spot basis monitoring; never assume equal prices.
- Exchange data licensing reviewed for the intended display and automated use.
- Failed critical gate => NO TRADE.

## Security
Provider API keys must live in backend environment variables or a secrets manager. Never commit keys to Git or ship them to browser JavaScript.
