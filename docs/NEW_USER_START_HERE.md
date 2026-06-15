# New User Start Here

This page is the shortest path for users who only want to call the package.

## Install

```bash
python -X utf8 -m pip install aquote-router
```

On Windows terminals, set UTF-8 first:

```bat
chcp 65001 >nul
python -X utf8 -m pip install aquote-router
```

## I Only Want Realtime Quotes

```python
from aquote_router import QuoteRouter

router = QuoteRouter.from_config(
    pytdx_servers_path="config/pytdx_servers.example.json",
    source_policy_path="config/source_policy.example.yaml",
)

records = router.realtime_quotes(["000001"])
print(records[0].to_dict())
```

CLI:

```bash
aquote-router realtime 000001 --json
```

Realtime APIs use pytdx first and may fall back to easyquotation Sina or Tencent
according to source policy.

## I Only Want 15-minute K-line

```python
bars = router.minute_kline("000001", period="15m", count=120)
print(bars[0].to_dict())
```

CLI:

```bash
aquote-router kline 000001 --period 15m --count 120 --json
```

K-line APIs are pytdx-only. They do not use easyquotation fallback.

## I Only Want Daily K-line

```python
bars = router.daily_kline("000001", count=120)
print(bars[0].to_dict())
```

CLI:

```bash
aquote-router kline 000001 --period 1d --count 120 --json
```

## K-line Timeout

First probe pytdx servers from the current network:

```bash
aquote-router probe-pytdx --json --output config/pytdx_servers.active.local.json
```

Then retry K-line with the active local pool:

```bash
aquote-router kline 000001 --period 15m --count 10 \
  --pytdx-servers config/pytdx_servers.active.local.json --json
```

Do not commit `config/pytdx_servers.active.local.json`. It is a local diagnostic
result and can change by network, region, and time.

## What Are source, source_level, and trace_id?

- `source` is the adapter that returned the record, such as `pytdx`,
  `easyquotation_sina`, or `easyquotation_tencent`.
- `source_level` is the configured pytdx server role, such as `primary`,
  `hot_backup`, or `backup`.
- `trace_id` ties a returned record to the audit log entry for the same routed
  request.

Use `trace_id` when reporting failures or matching CLI output with JSONL or
SQLite audit records.

## Read Next

1. [Quickstart](QUICKSTART.md)
2. [Data sources](DATA_SOURCES.md)
3. [K-line guide](KLINE_GUIDE.md)
4. [Return fields](RETURN_FIELDS.md)
5. [Troubleshooting](TROUBLESHOOTING.md)
6. [Issue guide](ISSUE_GUIDE.md)

## Boundary

This package is data access infrastructure. It does not provide investment
advice, account login, order execution, screening, timing signals, or
performance claims.
