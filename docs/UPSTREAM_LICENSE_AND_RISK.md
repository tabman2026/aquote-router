# Upstream License and Risk

`pyqauto` calls public Python libraries through adapters. It does not produce market data and does not claim official exchange-authorized data.

Current upstream dependencies:

- `pytdx`
- `easyquotation`

Users are responsible for reviewing upstream project licenses, service terms,
availability, and data quality before using results in their own systems.

Known risks:

- Upstream services may be delayed, unavailable, incomplete, or rate limited.
- Field names and units may change without notice.
- Realtime APIs allow fallback across sources; K-line APIs are pytdx-only.
- Cross-source comparison requires checking `source` and `source_level`.
