# Issue Guide

Use GitHub issues for reproducible package problems, documentation gaps, and
source failure reports. Keep reports small and include diagnostics that let a
maintainer separate local configuration, upstream source availability, and
package behavior.

## Installation Problems

Please include:

- `pyqauto` version you tried to install.
- Python version from `python -X utf8 --version`.
- OS name and terminal, for example Windows PowerShell or macOS Terminal.
- Full install command.
- Full error output.
- Output from:

```bash
python -X utf8 -m pip show pyqauto
```

On Windows, run:

```bat
chcp 65001 >nul
python -X utf8 -m pip show pyqauto
```

Do not include private credentials, account information, or local absolute paths
that are not needed to reproduce the problem.

## Data Source Failures

Please include:

- `pyqauto` version.
- Python version and OS.
- Full command or minimal Python code.
- API name, such as `realtime_quotes`, `minute_kline`, `daily_kline`, or
  `kline`.
- Symbol.
- `period` and `count` for K-line APIs, or `N/A` for realtime APIs.
- `trace_id` from CLI JSON output, returned records, or audit logs.
- Sanitized audit log snippet for the same `trace_id`.
- Output from `pyqauto diagnose --json`.
- Whether the problem happens every time or intermittently.

## K-line Timeout Reports

K-line APIs are pytdx-only. Before opening a K-line timeout issue, run:

```bash
pyqauto probe-pytdx --json --output config/pytdx_servers.active.local.json
```

Then retry with:

```bash
pyqauto kline 000001 --period 15m --count 10 \
  --pytdx-servers config/pytdx_servers.active.local.json --json
```

Include the sanitized `probe-pytdx` output in the issue. Do not commit or paste
the active local config file unless you have removed environment-specific
details.

## Sanitizing Audit Logs

Keep fields that help debugging:

- `trace_id`
- `api_name`
- `symbols`
- `started_at`, `finished_at`, and `duration_ms`
- `selected_source` and `selected_source_level`
- `fallback_chain`
- `attempts`
- `success`
- `error_type` and `error_message`
- `record_count`

Remove or redact:

- Private credentials or account identifiers.
- Local absolute paths and user names.
- Machine-specific directories.
- Any value unrelated to the failing call.

Do not include tokens, cookies, secrets, or account login data.

## Finding trace_id

Prefer CLI JSON output:

```bash
pyqauto realtime 000001 --json
```

For Python calls, inspect the returned model:

```python
import pyqauto as aq

record = aq.quote("000001")
print(record.trace_id)
```

If the call failed before returning records, find the matching audit log entry
by time and API name, then copy its `trace_id`.

## Running diagnose

`diagnose` checks local configuration and recent audit metadata. It does not
connect to upstream providers.

```bash
pyqauto diagnose --json
```

Include the full sanitized JSON output in source failure issues.

## Running probe-pytdx

`probe-pytdx` checks pytdx server connectivity and can write an active local
pool:

```bash
pyqauto probe-pytdx --json --output config/pytdx_servers.active.local.json
```

Useful fields in the output include connected server counts, K-line success
counts, tested symbol, tested minute period, and the active config path.

## Upstream Source or Package Problem?

Likely upstream or local network issue:

- `diagnose --json` shows valid local configuration.
- `probe-pytdx` cannot connect to any pytdx server from the current network.
- Realtime works through fallback but K-line fails because pytdx is unavailable.
- The same command works later without package changes.

Likely package issue:

- `diagnose --json` reports invalid bundled example config.
- A documented command fails before trying any source.
- Returned fields do not match [RETURN_FIELDS.md](RETURN_FIELDS.md).
- A failure is reproducible offline with a small fixture or fake adapter.

If unsure, open a data source failure issue and include `trace_id`,
`diagnose --json`, `probe-pytdx` for K-line cases, and a sanitized audit snippet.
