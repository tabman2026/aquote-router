# v0.4.0 Source Policy Draft

This file is a draft only. It does not modify the formal source policy and does
not change `config/source_policy.example.yaml`. Candidate adapters are not
directly enabled.

Candidate adapters are not directly enabled.

## Shared Rules

- Do not directly enable candidate adapter entries from this draft.
- Keep candidate rows behind mock tests, live probe, `unit_rules`, schema guard,
  and audit acceptance.
- Do not let rows with `unknown` units enter public records.
- Do not use easyquotation as a K-line fallback.

## 方案 A：保守方案

This is the recommended v0.4.0 planning baseline.

```text
realtime_quotes:
  pytdx -> easyquotation_sina -> easyquotation_tencent

kline:
  pytdx-only
```

Candidate adapters do not enter the default fallback chain. They can only be
used by manual research commands or isolated mock tests after implementation.

## 方案 B：研究方案

This is a research-only option and cannot be enabled directly.

```text
realtime_quotes:
  pytdx -> easyquotation_sina -> easyquotation_tencent -> efinance

daily_kline:
  pytdx -> efinance or baostock

minute_kline:
  pytdx -> efinance or baostock, pending capability validation
```

方案 B 不能直接启用，必须先通过 live probe、unit_rules、schema guard 和
audit 验收。Even after passing mock tests, any candidate adapter remains outside
the default chain until a separate source policy change is reviewed.

## Current Decision

Use 方案 A for current development. 方案 B stays as research text only.
