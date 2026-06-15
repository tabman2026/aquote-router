# Project State

Date: 2026-06-15

Version target: `0.2.0`

Implemented public APIs:

- `realtime_quotes`
- `full_realtime_quotes`
- `index_realtime`
- `minute_kline`
- `daily_kline`
- `kline`
- `diagnose`

Source policy status:

- Realtime APIs allow source fallback in the documented order.
- K-line APIs are pytdx-only.
- K-line supported periods are documented in source policy and K-line guide.

Validation status:

- pytest passed locally.
- Release scan and packaging checks are pending in this run.
