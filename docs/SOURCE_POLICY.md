# Source Policy

Source policy defines which adapter family may serve each public API and in what
order.

## Default Policy

```yaml
apis:
  realtime_quotes:
    allow_fallback: true
    fallback_order:
      - pytdx
      - easyquotation_sina
      - easyquotation_tencent

  full_realtime_quotes:
    allow_fallback: true
    fallback_order:
      - pytdx
      - easyquotation_sina
      - easyquotation_tencent

  index_realtime:
    allow_fallback: true
    fallback_order:
      - pytdx
      - easyquotation_sina
      - easyquotation_tencent

  minute_kline:
    allow_fallback: false
    fallback_order:
      - pytdx
    supported_periods:
      - 1m
      - 5m
      - 15m
      - 30m
      - 60m

  daily_kline:
    allow_fallback: false
    fallback_order:
      - pytdx
    supported_periods:
      - 1d

  kline:
    allow_fallback: false
    fallback_order:
      - pytdx
    supported_periods:
      - 1m
      - 5m
      - 15m
      - 30m
      - 60m
      - 1d
```

## pytdx Server Order

pytdx server entries are expanded by role:

1. `primary`
2. `hot_backup`
3. `backup`

Servers in the same role are sorted by `latency_ms` ascending.

## K-line Rule

`minute_kline`, `daily_kline`, and `kline` must remain pytdx-only. If all pytdx
servers fail, aquote-router raises `NoAvailableSourceError` and writes an audit
record with attempts and `fallback_chain`.
