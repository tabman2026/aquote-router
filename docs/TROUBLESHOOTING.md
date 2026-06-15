# Troubleshooting

Start with local diagnostics:

```bash
aquote-router diagnose --json
```

The command does not connect to upstream providers. It checks local config shape
and returns fields such as:

- `aquote_router_version`
- `source_policy_parseable`
- `source_policy_error_code`
- `pytdx_server_config_parseable`
- `enabled_sources`
- `supported_apis`
- `supported_kline_periods`
- `recent_trace_id`

## Common Checks

- Confirm `config/source_policy.example.yaml` parses.
- Confirm `config/pytdx_servers.example.json` contains enabled servers.
- Use `--json` on quote commands when table output is too narrow.
- Use audit `trace_id` to match CLI output to JSONL or SQLite records.
- For K-line failures, inspect pytdx attempts. K-line APIs do not use
  easyquotation fallback.

## Offline and Live Checks

Default tests are offline:

```bash
python -X utf8 -m pytest
```

Live smoke tests must be explicitly enabled:

```bash
set ENABLE_LIVE_SMOKE_TEST=1
python -X utf8 scripts/smoke_test.py
```
