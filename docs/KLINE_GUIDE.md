# K-line Guide

K-line APIs are pytdx-only in v0.2.0. They do not fall back to easyquotation.
When pytdx cannot return bars, the router raises a structured error and writes
audit attempts plus `fallback_chain`.

## Supported Periods

| API | Supported periods | Source |
|---|---|---|
| `minute_kline` | `1m`, `5m`, `15m`, `30m`, `60m` | `pytdx` |
| `daily_kline` | `1d` | `pytdx` |
| `kline` | `1m`, `5m`, `15m`, `30m`, `60m`, `1d` | `pytdx` |

`kline` also accepts `daily` and `day` as aliases for `1d`.

## Python Examples

15-minute bars:

```python
bars = router.minute_kline("000001", period="15m", count=120)
```

Daily bars:

```python
bars = router.daily_kline("000001", count=120)
```

Unified API:

```python
minute_bars = router.kline("000001", period="15m", count=120)
daily_bars = router.kline("000001", period="1d", count=120)
```

## CLI Examples

```bash
aquote-router minute 000001 --period 15m --count 120 --json
aquote-router daily 000001 --count 120 --json
aquote-router kline 000001 --period 1d --count 120 --json
```

## Return Model

K-line APIs return `KlineBar` objects with:

- `symbol`
- `datetime`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `amount`
- `period`
- `source`
- `source_level`
- `fallback_from`
- `is_fallback`
- `trace_id`
- `raw` when `include_raw=True`

`datetime` is the upstream pytdx bar timestamp serialized as a string. See
[RETURN_FIELDS.md](RETURN_FIELDS.md), [UNITS.md](UNITS.md), and
[TIME_AND_TRADING_DAY.md](TIME_AND_TRADING_DAY.md).

## Unsupported Features

Adjusted bars are not supported in v0.2.0. There is no front-adjusted or
back-adjusted K-line API unless a future release adds explicit fields, tests,
and documentation.
