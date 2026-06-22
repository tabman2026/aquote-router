# Unit Rules For Adapters

pyqauto adapters must normalize upstream units before public records are
returned.

## Standard Units

| Standard field | Standard unit | Rule |
|---|---|---|
| `volume_shares` | shares | All accepted quote and K-line rows use shares. |
| `amount_yuan` | yuan | All accepted quote and K-line rows use RMB yuan. |
| percent-like fields | percent number | `1.23` means `1.23%` unless a standard field explicitly says otherwise. |

## Required Conversions

1. If upstream volume is lots, convert lots to shares. 手转股 means
   `volume_shares = upstream_lots * 100`.
2. If upstream amount is already yuan, do not divide it by 100.
3. If upstream amount is ten-thousand-yuan, convert to yuan. 万元转元 means
   `amount_yuan = upstream_amount * 10000`.
4. Do not change a percent number such as `1.23` into `0.0123` unless the target
   standard field requires a ratio.

## Adapter Requirements

Each adapter must have `unit_rules`. Each `unit_rules` entry must be covered by
tests. A unit rule must include:

- upstream field;
- upstream unit;
- standard field;
- standard unit;
- conversion;
- test input;
- expected output.

## Examples

### AKShare Eastmoney Spot

| Upstream field | Upstream unit | Standard field | Standard unit | Conversion |
|---|---|---|---|---|
| `成交量` | lots | `volume_shares` | shares | multiply by 100 |
| `成交额` | yuan | `amount_yuan` | yuan | keep |

Important: AkShare `成交额` in this adapter is already yuan, so it must not be
divided by 100.

### easyquotation Tencent

Tencent realtime output can expose a composite value containing price,
lot-volume, and amount. Parse the composite field first, then write standard
fields:

| Composite part | Standard field | Conversion |
|---|---|---|
| price part | `price` | parse as yuan price |
| volume part | `volume_shares` | lots multiplied by 100 |
| amount part | `amount_yuan` | keep yuan |

Do not store a composite string in `volume_shares` or `amount_yuan`.

## Test Checklist

- One test proves lots become shares.
- One test proves yuan amount is kept as yuan.
- One test proves ten-thousand-yuan amount becomes yuan.
- One test proves missing unit input is rejected instead of filled with zero.
- One test proves percent-like values stay percent numbers when required.

