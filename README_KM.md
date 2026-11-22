# GVE Professional Order Flow Terminal — Frontend Foundation

## What this package contains
- `index.html`: Original uploaded ICT / XAUUSD application with the GVE Order Flow workspace appended.
- Existing ICT chart, analysis, signal, lessons/academy and settings code is preserved.
- New GVE workspace: Overview, Footprint CSV preview, Delta/CVD preview, Volume Profile status, DOM status, Setup Builder, Data Center and Risk.
- Setup configuration is stored in browser `localStorage`; export configuration JSON is supported.

## Important implementation boundaries
This is a frontend foundation, not a connected market-data system.
- Databento and Twelve Data are NOT connected in this package.
- The CSV importer accepts normalized CSV rows only. It does not parse Databento DBN files.
- Imported data is explicitly labelled UNVERIFIED. A CSV cannot prove exchange source, licensing, timestamp completeness or aggressor-side correctness.
- No true live Footprint, CVD, DOM, MBO reconstruction or Volume Profile is claimed.
- No API keys are requested in the browser.
- No MT5 orders are sent. `LIVE_TRADING_ENABLED=false` and `AUTO_EXECUTION_ENABLED=false`.

## Normalized trades CSV format
Required columns:
`timestamp,price,size,side`
Optional columns:
`symbol,provider,dataset,quality`

`side` accepts `BUY`, `SELL`, or `UNKNOWN`. Confirm the provider's aggressor-side convention before interpreting BUY/SELL as ask-/bid-initiated volume.

## Android usage
1. Download and extract the ZIP.
2. Open `index.html` using a browser or a local HTML viewer that supports JavaScript.
3. Use the `ICT Chart` tab for the original application.
4. Use `GVE Order Flow` for the new setup workspace.
5. Configuration is saved only in that browser on that device. Export the JSON file as a backup.

Some Android file viewers block local file scripts or browser storage. If the page does not work correctly, keep the files and open them later on a desktop browser or deploy to a trusted HTTPS host.

## Next engineering phases
1. Python backend and secure provider adapters.
2. Databento historical metadata, trades and MBP-10/MBO entitlement validation.
3. Twelve Data spot symbol/plan validation and UTC synchronization.
4. True Footprint / Delta / CVD / Volume Profile calculations with tests.
5. MBO order-book reconstruction and DOM visualization.
6. Replay, backtest, walk-forward and out-of-sample testing.
7. MT5 execution adapter only after all data, licensing, risk and test gates pass.


## Phase 2 — Python Core Engine
សូមមើល `backend/README_KM.md` សម្រាប់ការដំឡើង Backend, API និង Unit Tests។
