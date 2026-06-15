# Symbol Rules

Supported symbol formats:

- Six digits, such as `000001`, `399001`, or `600000`.
- Six digits plus `.SH` or `.SZ`, such as `600000.SH` or `000001.SZ`.

Bare prefixes are mapped as follows:

| Prefix | pytdx market |
|---|---|
| `0`, `3` | Shenzhen (`0`) |
| `5`, `6`, `9` | Shanghai (`1`) |

Unsupported formats raise `UnsupportedSymbolError` with code
`UNSUPPORTED_SYMBOL`.
