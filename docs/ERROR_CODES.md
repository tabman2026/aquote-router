# Error Codes

Error codes are stable public diagnostics used by exceptions, CLI output, and
audit records.

| Code | Meaning | Typical cause |
|---|---|---|
| `CONFIG_NOT_FOUND` | Required config file was not found. | A config path points to a missing file. |
| `CONFIG_PARSE_FAILED` | Config file could not be parsed. | Invalid JSON, YAML, or pytdx server shape. |
| `SOURCE_POLICY_NOT_FOUND` | Source policy file was not found. | `--config` points to a missing file. |
| `SOURCE_POLICY_INVALID` | Source policy content is invalid. | Missing API, unsupported source, or invalid K-line fallback policy. |
| `PYTDX_CONNECT_FAILED` | One pytdx server connection failed. | Network or server availability issue. |
| `PYTDX_ALL_SERVERS_FAILED` | All allowed pytdx servers failed. | Server pool unavailable or empty response from every pytdx attempt. |
| `EASYQUOTATION_SINA_FAILED` | Sina fallback source failed. | Upstream empty response or provider error. |
| `EASYQUOTATION_TENCENT_FAILED` | Tencent fallback source failed. | Upstream empty response or provider error. |
| `FALLBACK_EXHAUSTED` | Every allowed source failed. | No configured source returned records. |
| `SOURCE_POLICY_BLOCKED` | No source is enabled for the API. | Policy produced an empty adapter list. |
| `UNSUPPORTED_SYMBOL` | Symbol is outside documented rules. | Invalid suffix, length, or prefix. |
| `UNSUPPORTED_PERIOD` | K-line period is not supported. | Period is not one of the documented pytdx periods. |
| `EMPTY_RESPONSE` | A source returned no usable records. | Non-session time, unavailable server, or upstream behavior change. |
| `NORMALIZE_FAILED` | Upstream payload could not be normalized. | Field shape changed or values were invalid. |
| `AUDIT_WRITE_FAILED` | Audit sink could not be written. | Output directory or SQLite write failure. |
| `CLI_ARGUMENT_ERROR` | CLI arguments are invalid. | Missing argument or unsupported option combination. |

When reporting a source failure, include the error code, `trace_id`,
`fallback_chain`, and sanitized `pyqauto diagnose --json` output.
