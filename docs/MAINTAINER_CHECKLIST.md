# Maintainer Checklist

Use this checklist to keep issue triage, patches, and releases consistent.

## Issue Triage

1. Start with the reported `trace_id`.
2. Match the `trace_id` to JSONL or SQLite audit records.
3. For data source failures, inspect `pyqauto diagnose --json` output
   before assuming a package bug.
4. For K-line failures, ask the user to run:

```bash
pyqauto probe-pytdx --json --output config/pytdx_servers.active.local.json
```

5. Check whether the failing API is realtime or K-line. Realtime can use
   easyquotation fallback; K-line is pytdx-only.
6. Confirm whether the issue is reproducible outside the reporter's local
   network and time window.

## Patch Policy

1. Ship a patch only for package code, packaging metadata, documentation
   breakage, or bundled config problems.
2. Do not ship a patch only because a public upstream source is temporarily
   unavailable.
3. Do not change source policy, field standards, or audit log structure without
   updating README, `docs/SOURCE_POLICY.md`, and `PROJECT_STATE.md`.
4. Add adapter unit tests and field normalization tests before adding any real
   data source.
5. Consider a minor version for a new adapter or public API addition.
6. Use a patch version for compatible bug fixes or packaging/doc corrections
   that must reach PyPI.

## Release Gate

Before publishing any release, run:

```bash
python -X utf8 -m pytest -q
python -X utf8 -m ruff check .
python -X utf8 scripts/check_release.py
python -X utf8 scripts/smoke_test.py
python -X utf8 -m build
```

On Windows, run `chcp 65001 >nul` first.

Also check:

```bash
pyqauto --help
pyqauto diagnose --json
pyqauto probe-pytdx --help
```

Live smoke checks must stay opt-in:

```bash
set ENABLE_LIVE_SMOKE_TEST=1
python -X utf8 scripts/smoke_test.py
```

## Post-release

1. Verify GitHub Release notes are clear.
2. Verify PyPI README rendering and Project links.
3. Run a cold-start install in a clean environment.
4. Confirm CLI help, `diagnose --json`, and `probe-pytdx --help` work after
   installation.
5. Confirm no local active pytdx pool, logs, JSONL, SQLite files, virtual
   environments, or local reports were included in the release artifacts.

## Non-goals

Do not add account login, order execution, screening workflows, timing signals,
or performance claims to this project.
