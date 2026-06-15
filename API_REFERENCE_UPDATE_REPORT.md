# API Reference Update Report

Date: 2026-06-15

## Updated

- Added `docs/API_REFERENCE.md`.
- Added `docs/CLI_REFERENCE.md`.
- Added `docs/QUICKSTART.md`.
- Updated `README.md` links to core docs.
- Updated `docs/KLINE_GUIDE.md` for 15-minute, daily, and unified K-line usage.
- Updated `docs/DATA_SOURCES.md` to match actual source routing.
- Updated `docs/RETURN_FIELDS.md` for `QuoteRecord` and `KlineBar`.
- Updated `docs/UNITS.md` for K-line volume and amount conventions.

## API Coverage

- `from_config`: documented.
- `realtime_quotes`: documented.
- `full_realtime_quotes`: documented.
- `index_realtime`: documented.
- `minute_kline`: documented.
- `daily_kline`: documented.
- `kline`: documented.
- `diagnose`: documented with CLI entry.

## Validation

- pytest: passed locally.
- API/code consistency report: generated.
- K-line fallback rule: documented as pytdx-only.
