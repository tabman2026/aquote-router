# Pytdx Server Pool Refresh Report

Created at: 2026-06-15T11:56:30Z

## Path Audit

- Repository root: `pyqauto`
- Required repository markers found: `pyproject.toml`, `README.md`, `pyqauto/__init__.py`, `.github/workflows/`, `docs/`, `scripts/`
- Task018 files were found in the parent workspace instead of the repository root.
- `scripts/live_check.py` was copied to `scripts/live_check.py`.
- `docs/LIVE_CHECK.md` was copied to `docs/LIVE_CHECK.md`.
- `logs/` audit outputs are ignored by git.
- `config/pytdx_servers.active.local.json` and `config/pytdx_servers.local.json` are ignored by git.
- Public docs and reports use repository-relative paths only.

## Pytdx Server Probe

- Original example server pool count: 3
- Official pytdx package sources read:
  - `pytdx.config.hosts.hq_hosts`: 104 candidates
  - `pytdx.util.best_ip.stock_ip`: 60 candidates
- De-duplicated official pool count: 147
- Probed server count: 147
- Connect success count: 36
- Realtime quote success count: 36
- Minute kline success count: 36
- Daily kline success count: 36
- Fastest available server: `119.29.19.242:7709`, latency `102.453 ms`
- Generated active local config: yes
- Active local config path: `config/pytdx_servers.active.local.json`
- Active local config server count: 10

The active config is a local diagnostic result. It is not treated as a stable
public configuration because upstream pytdx server availability changes.

## Live Check Rerun

- Command: `python -X utf8 scripts\live_check.py --json --config config\pytdx_servers.active.local.json`
- Result: PASS
- `realtime_quotes`: PASS, real source `pytdx`
- `full_realtime_quotes`: PASS, real source `pytdx`
- `index_realtime`: PASS, real source `pytdx`
- `minute_kline` 15m: PASS, real source `pytdx`
- `daily_kline`: PASS, real source `pytdx`
- Unified `kline` 15m and 1d: PASS, real source `pytdx`
- JSONL audit output: `logs/live_check_audit.jsonl`
- SQLite audit output: `logs/live_check_audit.sqlite3`
- JSONL audit records total after rerun: 50
- SQLite audit rows after rerun: 50 audit rows, 285 attempt rows

The exact default CLI kline commands still fail when they use
`config/pytdx_servers.example.json`, because that example pool points to stale
servers. The same CLI kline commands pass when run with
`--pytdx-servers config\pytdx_servers.active.local.json`.

## Release Decision

- Requires v0.2.1: no
- Reason: no public API change, CLI parameter bug, daily/minute kline implementation
  bug, source policy loading bug, package missing-file issue, or misleading public
  docs issue was found.
- The observed failure mode is stale upstream pytdx server availability in the
  default example pool, recovered by a local active pool refresh.
- No new tag was created.
- No PyPI publish was performed.

## Boundaries

This task did not add an API service, data redistribution service, account login,
order execution, screening workflow, timing signal, position sizing, return
promise, win-rate claim, or investment advice workflow.
