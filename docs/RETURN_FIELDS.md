# Return Fields

The public return models are `QuoteRecord` for realtime APIs and `KlineBar` for
K-line APIs.

## QuoteRecord

Used by `realtime_quotes`, `full_realtime_quotes`, and `index_realtime`.

| Field | Meaning |
|---|---|
| `symbol` | Six-digit symbol code after normalization. |
| `name` | Upstream display name when available. |
| `price` | Current price. |
| `open` | Session open price. |
| `high` | Session high price. |
| `low` | Session low price. |
| `pre_close` | Previous close when available. |
| `volume` | Upstream numeric volume value, converted to `float` when possible. |
| `amount` | Upstream numeric amount value, converted to `float` when possible. |
| `datetime` | Upstream timestamp string. |
| `source` | Selected adapter: `pytdx`, `easyquotation_sina`, or `easyquotation_tencent`. |
| `source_level` | pytdx server role: `primary`, `hot_backup`, or `backup`; usually empty for easyquotation. |
| `fallback_from` | Last failed source before the selected source. |
| `is_fallback` | `True` when one or more earlier sources failed. |
| `raw` | Upstream payload when `include_raw=True`; omitted from `to_dict()` by default. |
| `error` | Record-level error field, normally empty. |
| `trace_id` | Audit correlation id for this router call. |

## KlineBar

Used by `minute_kline`, `daily_kline`, and `kline`.

| Field | Meaning |
|---|---|
| `symbol` | Six-digit symbol code after normalization. |
| `datetime` | pytdx bar timestamp string. |
| `open` | Bar open price. |
| `high` | Bar high price. |
| `low` | Bar low price. |
| `close` | Bar close price. |
| `volume` | pytdx numeric volume value, converted to `float` when possible. |
| `amount` | pytdx numeric amount value, converted to `float` when possible. |
| `period` | Requested normalized period, such as `15m` or `1d`. |
| `source` | Always `pytdx` for returned K-line bars in v0.2.0. |
| `source_level` | pytdx server role: `primary`, `hot_backup`, or `backup`. |
| `fallback_from` | Last failed pytdx server role before the selected server. |
| `is_fallback` | `True` when an earlier pytdx server failed. |
| `raw` | pytdx row when `include_raw=True`; omitted from `to_dict()` by default. |
| `error` | Record-level error field, normally empty. |
| `trace_id` | Audit correlation id for this router call. |

`KlineBar.price` is a compatibility property that returns `close`.
