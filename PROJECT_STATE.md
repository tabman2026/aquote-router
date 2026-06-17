# Project State

Date: 2026-06-18

Version target: `0.3.0`

Current release task status:

- Project brand, PyPI package name, import package, CLI command, and GitHub
  repository are renamed to `pyqauto`.
- The old `aquote-router` package and `aquote_router` import path are no longer
  the recommended installation or import path.
- Default source policy and example pytdx server pool remain bundled as package data.
- The `pyqauto` import package exposes simple module-level functions for default use.
- `QuoteRouter.from_config()` can be called without config path arguments.
- Legacy example paths under `config/` fall back to packaged defaults when the
  caller's project does not have those files.
- Public examples now use the zero-config constructor path by default.

Implemented public APIs:

- `realtime_quotes`
- `full_realtime_quotes`
- `index_realtime`
- `minute_kline`
- `daily_kline`
- `kline`
- `diagnose`
- `probe-pytdx`

Source policy status:

- Realtime APIs allow source fallback in the documented order.
- K-line APIs are pytdx-only.
- K-line supported periods are documented in source policy and K-line guide.
- `probe-pytdx` writes a local active pytdx pool for diagnostics only.

Validation status:

- pytest passed locally for v0.3.0 rename task.
- ruff passed locally for v0.3.0 rename task.
- Release scan passed locally for v0.3.0 rename task.
- Offline smoke test passed locally for v0.3.0 rename task.
- Build passed locally for v0.3.0 rename task.
- The v0.3.0 task keeps public quote and K-line behavior unchanged under the
  new `pyqauto` name.
- The active local pytdx pool is ignored by Git and excluded from release files.
- GitHub repository rename to `tabman2026/pyqauto`: completed.
- GitHub Release v0.3.0: completed.
- PyPI pyqauto 0.3.0: blocked by PyPI Trusted Publishing `invalid-publisher`.
- Post-release cold-start smoke test: blocked until PyPI publication completes.
