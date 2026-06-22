# Field Mapping Template

Copy this table into an adapter design note before implementing a new source.
Fill every row from official upstream documentation or a bounded raw schema
probe.

| 上游字段 | 上游含义 | 上游单位 | pyqauto 标准字段 | 标准单位 | 是否核心字段 | 缺失处理 | 示例值 |
|---|---|---|---|---|---|---|---|
| code | Symbol code | source format | symbol | normalized symbol | yes | reject row | 000001.SZ |
| name | Security name | text | name | text | no | keep null | 平安银行 |
| latest | Latest quote price | yuan | price | yuan | yes for quote | reject row | 10.50 |
| open | Open price | yuan | open | yuan | yes | reject row | 10.10 |
| high | High price | yuan | high | yuan | yes | reject row | 10.80 |
| low | Low price | yuan | low | yuan | yes | reject row | 10.00 |
| pre_close | Previous close | yuan | pre_close | yuan | yes | reject row | 10.20 |
| volume | Volume | confirm from upstream | volume_shares | shares | yes | reject row | 123400 |
| amount | Amount | confirm from upstream | amount_yuan | yuan | yes | reject row | 12345678.90 |
| trade_time | Quote or bar time | source timestamp | datetime | ISO-like string | yes | use fetch time only when policy allows | 2026-01-01 09:31:00 |
| period | K-line period | source period | period | pyqauto period | yes for K-line | reject row | 15m |
| source | Source id | text | source | text | yes | set from adapter | example_source |
| source_level | Source role | text | source_level | text or null | no | set null when not applicable | backup |
| trace_id | Request id | text | trace_id | text | yes | set by router | trace-001 |
| raw | Bounded raw row | object | raw | object | no | include only when requested | {"code": "000001"} |

## Required Mapping Notes

For every adapter, add:

- source API name;
- raw return type;
- symbol conversion rule;
- period conversion rule for K-line adapters;
- adjustment rule for K-line adapters;
- volume rule;
- amount rule;
- percent-like field rule;
- validation rejection rule.

## Review Checklist

- Every core standard field has a mapped upstream field or an explicit policy
  reason.
- `volume_shares` is in shares.
- `amount_yuan` is in yuan.
- Missing price, volume, amount, or timestamp fields are rejected.
- Raw rows are not public records until validation passes.
