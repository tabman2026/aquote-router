# Units

The router performs lightweight type normalization only. It does not rescale
volume or amount across sources.

## QuoteRecord

| Field | Unit or convention |
|---|---|
| `price` | RMB yuan. |
| `open` | RMB yuan. |
| `high` | RMB yuan. |
| `low` | RMB yuan. |
| `pre_close` | RMB yuan when available. |
| `volume` | Upstream numeric volume value as returned by the selected source. |
| `amount` | Upstream numeric amount value as returned by the selected source. |
| `datetime` | Upstream timestamp string. |

## KlineBar

| Field | Unit or convention |
|---|---|
| `open` | RMB yuan. |
| `high` | RMB yuan. |
| `low` | RMB yuan. |
| `close` | RMB yuan. |
| `volume` | pytdx numeric volume value, converted to `float` when possible. |
| `amount` | pytdx numeric amount value, converted to `float` when possible. |
| `datetime` | pytdx bar timestamp string. |
| `period` | Normalized request period: `1m`, `5m`, `15m`, `30m`, `60m`, or `1d`. |

`pct_chg` is not a standard field in v0.2.0. If an upstream payload contains it,
it is preserved only inside `raw` when `include_raw=True`.
