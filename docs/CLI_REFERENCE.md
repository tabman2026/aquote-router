# CLI Reference

Global options:

```bash
aquote-router --config config/source_policy.example.yaml \
  --pytdx-servers config/pytdx_servers.example.json \
  --audit-jsonl logs/aquote_router_audit.jsonl \
  --audit-sqlite logs/aquote_router_audit.sqlite3 \
  COMMAND
```

`--json` can be passed globally before the command or on supported commands
after command arguments.

## Commands

```bash
aquote-router realtime 000001 600000
aquote-router full 000001 600000
aquote-router full-realtime 000001 600000
aquote-router index 000001 399001
aquote-router minute 000001 --period 15m --count 120
aquote-router daily 000001 --count 120
aquote-router kline 000001 --period 15m --count 120
aquote-router kline 000001 --period 1d --count 120
aquote-router diagnose --json
```

All commands support `--help`. Quote and K-line commands support `--json`.
JSON output includes `source`, `source_level`, and `trace_id`.

Failures return a non-zero exit code and include the project error code, for
example `[UNSUPPORTED_PERIOD]`.
