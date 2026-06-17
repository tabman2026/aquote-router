from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_user_start_here_covers_minimal_paths() -> None:
    text = (ROOT / "docs" / "NEW_USER_START_HERE.md").read_text(encoding="utf-8")

    for expected in [
        "realtime_quotes",
        'period="15m"',
        "daily_kline",
        "probe-pytdx",
        "source_level",
        "trace_id",
        "DATA_SOURCES.md",
    ]:
        assert expected in text


def test_issue_guide_requests_diagnostics_and_sanitized_logs() -> None:
    text = (ROOT / "docs" / "ISSUE_GUIDE.md").read_text(encoding="utf-8")

    for expected in [
        "pyqauto diagnose --json",
        "pyqauto probe-pytdx --json",
        "trace_id",
        "Sanitizing Audit Logs",
        "Upstream Source or Package Problem?",
    ]:
        assert expected in text


def test_maintainer_checklist_keeps_release_gate_visible() -> None:
    text = (ROOT / "docs" / "MAINTAINER_CHECKLIST.md").read_text(encoding="utf-8")

    for expected in [
        "python -X utf8 -m pytest -q",
        "python -X utf8 -m ruff check .",
        "python -X utf8 scripts/check_release.py",
        "python -X utf8 scripts/smoke_test.py",
        "python -X utf8 -m build",
        "PyPI",
        "cold-start",
    ]:
        assert expected in text
